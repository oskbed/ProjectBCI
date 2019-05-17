#!/usr/bin/env python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-


# ----------------------------------------------------------------------------#
#                  OpenBCI Cyton CCA Application                              #
# ----------------------------------------------------------------------------#


import sys
import os

OpenBCI_PATH = '/Users/oskar.bedychaj/University/OpenBCI_Python'

# // Load OpenBCI_Python to $PATH variable. //
sys.path.insert(0, OpenBCI_PATH)

from sklearn.cross_decomposition import CCA
import numpy as np
import multiprocessing as mp
import test as bci
import scipy.signal as sig
import time
#import matplotlib.pyplot as plt
from time import gmtime, strftime
import csv


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
        GUI Mode on/off

    """
    def __init__(self, sampling_rate=256, connect=True, port='', channels=[],
    path='', test_session=True, electrodes=2, time_run=10, mode=1, save=False, subj=0):

        self.CHANNELS = channels
        self.PATH = path

        self.bci_port = port
        self.connect = connect

        self.electrodes = electrodes
        self.time_run = time_run
        self.mode = mode
        self.save_to_file = save
        self.subj = 0

        self.reference_signals = []

        self.__fs = 1./sampling_rate
        self.__t = np.arange(0.0, 1.0, self.__fs)

        self.test_session = test_session

        self.board = bci.OpenBCISimulator(channels=[0,1], subj=subj)
        #self.board.print_register_settings()
        #self.sampling_rate = int(self.board.getSampleRate())
        self.sampling_rate = sampling_rate

        print ("================================")
        print ("  OpenBCI Cyton CCA Application ")
        print ("================================")

        self.streaming = mp.Event()
        self.terminate = mp.Event()

    def initialize(self):
        self.prcs = mp.Process(target=self.split,
                               args=(self.reference_signals,))
        self.prcs.daemon = True
        self.prcs.start()

    def add_stimuli(self, hz):
        '''Add stimuli to generate artificial signal'''

        self.hz = hz
        self.reference_signals.append(SignalReference(self.hz, self.__t))
        print ("Stimuli of {} hz added!".format(self.hz))

    def decission(self):
        status = input("Press Enter to start... ")

        if self.connect:
            self.initialize()

        # Compensate for packet correlation
        time.sleep(self.time_run+1)
        print("".join(["=" for x in range(32)]))
        print("END OF TRIAL")
        print("".join(["=" for x in range(32)]))
        self.prcs.terminate()
        #self.terminate.clear()


        if self.terminate.is_set():
            self.prcs.terminate()
            self.terminate.clear()


    def split(self, ref_signals):

        self.ref = ref_signals

        def handle_sample(sample):
            ''' Save samples into table; single process '''

            self.correlation.acquire_data(sample.channel_data[:self.electrodes])

            # Set termination
            if self.terminate.is_set():
                self.streaming.clear()
                self.board.stop()


        # Board connection #

        self.correlation = CrossCorrelation(self.sampling_rate,
                                            self.electrodes,
                                            self.ref,
                                            self.save_to_file,
                                            self.subj)

        self.board.start_streaming(handle_sample)
        #self.board.disconnect()

class SignalReference(object):
    """ Reference signal generator"""
    def __init__(self, hz, t):

        self.hz = hz

        self.reference = np.zeros(shape=(len(t), 8))

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
    def __init__(self, sampling_rate, channels_num, ref_signals, save_to_file, subj):
        self.signal_file = []
        self.packet_id = 0
        self.all_packets = 0
        self.sampling_rate = sampling_rate
        self.rs = ref_signals
        self.sampling_rate = sampling_rate
        self.channels_num = channels_num
        self.save_to_file = save_to_file
        self.signal_window = np.zeros(shape=(sampling_rate, channels_num))
        self.channels = np.zeros(shape=(len(self.rs), 3), dtype=tuple)
        self.ssvep_display = np.zeros(shape=(len(self.rs), 1), dtype=int)
        self.logging = []
        self.channels_list = []
        self.flt = OnlineFilter()



        self.text_file = open("/Users/oskar.bedychaj/University/stimuli/badanie" + str(subj) + ".txt", 'r')
        self.data_stimulus = self.text_file.read().split(',')
        del self.data_stimulus[-1]
        self.stim_array = []

        for i in self.data_stimulus:
            for j in range(5):
                self.stim_array.append(i)

        self.stim_array.append(self.stim_array[-1])
        self.hits = 0


    def acquire_data(self, packet):
        self.signal_window[self.packet_id] = self.filtering(packet)
        self.packet_id += 1

        if self.packet_id % self.sampling_rate == 0:
            self.all_packets += 1
            #filtered = self.filtering(self.signal_window)
            if self.save_to_file:
                self.save_file(np.squeeze(np.array(self.signal_window)))
                self.save_file(self.channels)

            self.correlate(self.signal_window)
            self.make_decission()
            self.print_results(self.stim_array[self.all_packets])
            self.packet_id = 0

    def save_file(self, list_file):

        if list_file.shape == (self.sampling_rate, self.channels_num):
            myFile = open('outputs/signal_filtered' + '.csv', 'a')

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
        #packet = np.squeeze(np.array(packeqt))
        #packet = np.array(packet)
       # print("========")
        #print ("1", packet)
        for i in range(self.channels_num):
            packet[i] = self.flt.filterIIR(packet[i], i)

        #time.sleep(1)
        #print ("2",packet)
        return packet
        

    def correlate(self, signal):
        for ref in range(len(self.rs)):
            sample = signal

            cca = CCA(n_components=1)

            ref_all = self.rs[ref].reference[:, [0, 1, 2, 3]]
           
            cca.fit(sample, ref_all)

            u, v = cca.transform(sample, ref_all)

            corr = abs(np.corrcoef(u.T, v.T)[0, 1])
            self.channels_list.append(corr)
            self.channels[ref] = corr
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

        # max = 0
        # index = 0
        # for i in range(len(self.channels)):
        #     if (self.channels[i][2]) > max:
        #         max = self.channels[i][2]
        #         index = i
        print(self.channels_list.index(max(self.channels_list)))
        #print (index)
        #print (max)
        #print (self.stim_array[self.all_packets])

        # if (index + 1) == int(self.stim_array[self.all_packets]):
        #     print("Zgodny")
        #     self.hits += 1

    def print_results(self,stimul):
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
        print("Displayed stimuli: ", int(stimul))
        print("========")
        print("Global hits: ", self.hits)
