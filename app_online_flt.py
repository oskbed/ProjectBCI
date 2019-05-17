#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-


# ----------------------------------------------------------------------------#
#                  OpenBCI Cyton CCA Application                              #
# ----------------------------------------------------------------------------#
#TODO SAVE RAW SIGNAL TO RAM

import sys
import os

OpenBCI_PATH = os.getcwd() + '/OpenBCI_Python'

# // Load OpenBCI_Python to $PATH variable. //
sys.path.insert(0, OpenBCI_PATH)

from sklearn.cross_decomposition import CCA
import numpy as np
import multiprocessing as mp
import openbci.cyton as bci
import scipy.signal as sig
import time
#import matplotlib.pyplot as plt
from time import gmtime, strftime
import csv
import serial


class CcaLive(object):
    """CCA Application for SSVEP detection.

    Parameters
    ----------
    sampling_rate : integer
        Sampling rate of device. Default 256 or 250 (for OpenBCI_Ganglion).
    connect : bool
        Connect to device immediately after object initialization.
    port : string
        MAC Address of a device.
    test_session : bool
        Whether to keep real time processing of packets.
    gui : bool
        GUI wyniki on/off

    """
    def __init__(self, sampling_rate=250, connect=True, port='',
    port_arduino=None, electrodes=2, time_run=10, save=False, bandpass=None):

        self.bci_port = port
        self.connect = connect

        self.electrodes = electrodes
        self.time_run = time_run
        self.save_to_file = save
        self.port_arduino = port_arduino

        self.reference_signals = []

        self.__fs = 1./sampling_rate
        self.__t = np.arange(0.0, 1.0, self.__fs)

        self.board = bci.OpenBCICyton(port=self.bci_port)
        self.board.print_register_settings()
        self.sampling_rate = sampling_rate
        self.bandpass = bandpass

        print ("================================")
        print ("  OpenBCI Cyton CCA Application ")
        print ("================================")

        self.streaming = mp.Event()
        self.terminate = mp.Event()

        # if self.port_arduino != None:
        #     self.serial_arduino = serial.Serial(self.port_arduino, 9600)
        #     time.sleep(2)
        #     self.serial_arduino.write(b"H")

    def initialize(self):
        self.prcs = mp.Process(target=self.split,
                               args=(self.reference_signals,))
        self.prcs.daemon = True
        self.prcs.start()

    def add_stimuli(self, hz):
        '''Add stimuli to generate artificial signal'''

        self.hz = hz
        self.reference_signals.append(SignalReference(self.hz, self.__t))
        print ("Stimuli {} hz added!".format(self.hz))

    def decission(self):
        status = input("Press Enter to start... ")
        # if self.port_arduino:
        #     self.serial_arduino.write(b"L")

        if self.connect:
            self.initialize()

        if self.port_arduino:
            time.sleep(5)
            #self.serial_arduino.write(b"L")


        # Compensate for packet correlation
        time.sleep(self.time_run+1)
        print("".join(["=" for x in range(32)]))
        print("END OF TRIAL")
        print("".join(["=" for x in range(32)]))
        self.prcs.terminate()
        #self.terminate.clear()


        if self.terminate.is_set():
            self.prcs.terminate()
            serial.Serial(self.port_arduino, 9600).close()
            self.terminate.clear()


    def split(self, ref_signals):

        self.ref = ref_signals

        def handle_sample(sample):
            ''' Save samples into table; single process '''

            self.correlation.acquire_data(sample.channel_data[:self.electrodes])

            # Set termination
            if self.terminate.is_set():
                serial.Serial(self.port_arduino, 9600).close()
                self.streaming.clear()
                self.board.stop()


        # Board connection #

        self.correlation = CrossCorrelation(self.sampling_rate,
                                            self.bandpass,
                                            self.electrodes,
                                            self.ref,
                                            self.save_to_file,
                                            self.port_arduino)

        self.board.start_streaming(handle_sample)
        self.board.disconnect()

class SignalReference(object):
    """ Reference signal generator"""
    def __init__(self, hz, t):

        self.hz = hz

        self.reference = np.zeros(shape=(len(t), 6))

        self.reference[:, 0] = np.array([np.sin(2*np.pi*i*self.hz) for i in t]) # sin
        self.reference[:, 1] = np.array([np.cos(2*np.pi*i*self.hz) for i in t]) # cos
        self.reference[:, 2] = np.array([np.sin(2*np.pi*i*self.hz*2) for i in t]) #
        self.reference[:, 3] = np.array([np.cos(2*np.pi*i*self.hz*2) for i in t]) #
        self.reference[:, 4] = np.array([np.sin(2*np.pi*i*self.hz*0.5) for i in t]) #
        self.reference[:, 5] = np.array([np.cos(2*np.pi*i*self.hz*0.5) for i in t]) #


class OnlineFilter(object):
    def __init__(self):
        self.prev_x = np.zeros((8, 5))
        self.prev_y = np.zeros((8, 5))
        self.prev_x2 = np.zeros((8, 5))
        self.prev_y2 = np.zeros((8, 5))

    def filterIIR(self, data, nrk):

        b = np.array([
                0.1750876436721012,
                0,
                -0.3501752873442023,
                0,
                0.1750876436721012
            ])
        a = np.array([
                1,
                -2.299055356038497,
                1.967497759984450,
                -0.8748055564494800,
                0.2196539839136946
            ])

        # 50 hz 
        b2 = np.array([
            0.96508099,
            -1.19328255,
            2.29902305,
            -1.19328255,
            0.96508099
        ])

        a2 = np.array([
            1,
            -1.21449347931898,
            2.29780334191380,
            -1.17207162934772,
            0.931381682126902
        ])

        j = 5 - 1
        while j > 0:
            self.prev_x[nrk, j] = self.prev_x[nrk, j - 1]
            self.prev_y[nrk, j] = self.prev_y[nrk, j - 1]
            self.prev_x2[nrk, j] = self.prev_x2[nrk, j - 1]
            self.prev_y2[nrk, j] = self.prev_y2[nrk, j - 1]
            j -= 1

        self.prev_x[nrk, 0] = data

        filtered = self.filter_data(b2, a2, b, a, nrk)
        return filtered


    def filter_data(self, b2, a2, b, a, nrk):
        value = 0.0
        for j in range(5):
            value += b2[j] * self.prev_x[nrk, j]
            if j > 0:
                value -= a2[j] * self.prev_y[nrk, j]
        self.prev_y[nrk, 0] = value
        self.prev_x2[nrk, 0] = value
        value = 0.0
        for j in range(5):
            value += b[j] * self.prev_x2[nrk, j]
            if j > 0:
                value -= a[j] * self.prev_y2[nrk, j]
        self.prev_y2[nrk, 0] = value
        return value


class CrossCorrelation(object):
    """CCA class; returns correlation value for each channel """
    def __init__(self, sampling_rate, filters, channels_num, ref_signals, save_to_file, port_arduino):
        self.signal_file = []
        self.packet_id = 0
        self.all_packets = 0
        self.port_arduino = port_arduino
        self.sampling_rate = sampling_rate
        self.rs = ref_signals
        self.sampling_rate = sampling_rate
        self.channels_num = channels_num
        self.save_to_file = save_to_file
        self.signal_window = np.zeros(shape=(sampling_rate, channels_num))
        self.channels = np.zeros(shape=(len(self.rs), 3), dtype=tuple)
        self.ssvep_display = np.zeros(shape=(len(self.rs), 1), dtype=int)
        self.logging = []
        self.raw_signal = 0 # TODO: Load entire signal to RAM and save afterwards.

        self.flt = OnlineFilter()
        self.serial_arduino = serial.Serial(self.port_arduino, 9600)
        time.sleep(2)
        self.serial_arduino.write(b"H")

        # if filters == None:
        #     if self.rs[-1].hz >= 49:
        #         self.filter = ((int(self.rs[0]) - 2), (49))
        #     else:
        #         self.filter = ((int(self.rs[0].hz) - 2), ((int(self.rs[-1].hz)*2) + 4))
        # else:
        #     self.filter = filters

        #print("Bandpass filter set to: ", self.filter[0], "/", self.filter[1])

    def acquire_data(self, packet):
        self.signal_window[self.packet_id] = self.filtering(packet)
        self.signal_file.append(packet)
        self.packet_id += 1

        if self.packet_id % self.sampling_rate == 0:
            self.serial_arduino.write(b"H")
            self.all_packets += 1
            #filtered = self.filtering(self.signal_window)
            if self.save_to_file:
                self.save_file(np.squeeze(np.array(packet)))  # Is that good?
                self.save_file(self.channels)

            self.correlate(self.signal_window)
            self.make_decission()
            self.print_results()
            self.packet_id = 0

    def save_file(self, list_file):

        if list_file.shape == (self.sampling_rate, self.channels_num):
            myFile = open('outputs/signal_raw' + '.csv', 'a')

            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(list_file)


        elif list_file.shape == (len(self.rs), 3):
            myFile = open('outputs/results' + '.csv', 'a')

            with myFile:
                writer = csv.writer(myFile)
                writer.writerows(list_file)
        else:
            pass

    def filtering(self, packet):
        """ Push single sample into the list """
        for i in range(self.channels_num):
            packet[i] = self.flt.filterIIR(packet[i], i)

        return packet


    def correlate(self, signal):
        for ref in range(len(self.rs)):
            sample = signal

            cca = CCA(n_components=1)
            cca_ref = CCA(n_components=1)
            cca_all = CCA(n_components=1)

            ref_ = self.rs[ref].reference[:, [0, 1, 2, 3]]
            ref_2 = self.rs[ref].reference[:, [0, 1, 4, 5]]
            ref_all = self.rs[ref].reference[:, [0, 1, 2, 3]]

            cca.fit(sample, ref_)
            cca_ref.fit(sample, ref_2)
            cca_all.fit(sample, ref_all)

            u, v = cca.transform(sample, ref_)
            u_2, v_2 = cca_ref.transform(sample, ref_2)
            u_3, v_3 = cca_all.transform(sample, ref_all)

            corr = np.corrcoef(u.T, v.T)[0, 1]
            corr2 = np.corrcoef(u_2.T, v_2.T)[0, 1]
            corr_all = np.corrcoef(u_3.T, v_3.T)[0, 1]
            self.channels[ref] = corr, corr2, corr_all
            #self.channels[ref] = corr_all

    def make_decission(self):
        '''Simple SSVEP Classifier'''
        # TODO: Improve ERP detection.
        best_ = 0
        it_ = 0
        for ref in range(len(self.rs)):
            thereshold_01 = self.channels[ref][2] >= 0.375
            thereshold_02 = self.channels[ref][1] >= 0.22
            if thereshold_01 and thereshold_02:
                if self.channels[ref][0] >= best_:
                    best_ = self.channels[ref][0]
                    it_ = ref
                    self.ssvep_display[it_] = 1
                else:
                    self.ssvep_display[ref] = 0
            else:
                self.ssvep_display[ref] = 0

        self.logging.append(self.ssvep_display.copy())

    def print_results(self):
        ''' Prints results in terminal '''
        print("================================")
        print("Packet ID : %s " % self.all_packets)
        print("================================")
        print("Canonical Correlation:")
        for i in range(len(self.rs)):
            print("Signal {hz}: {channel_value:.3}".format(hz=(str(self.rs[i].hz) + " hz"), channel_value=
                  self.channels[i][2]))
        print("Stimuli detection: {0}".format([str(self.ssvep_display[i])
              for i in range(len(self.ssvep_display))]))
