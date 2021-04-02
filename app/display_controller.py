import pickle
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM, gethostname, timeout
from utils import logger, receive_through_socket, SocketTimeout
import multiprocessing as mp 
import logging
import sys
import os
from psychopy import visual, event, core
import ast
from numpy import sin, pi
from time import sleep

DISPLAY_REFRESH_RATE = 60
DISPLAY_SOCKET_ADDRESS = gethostbyname(gethostname())
DISPLAY_SOCKET_PORT = 2093
DISPLAY_BUFFER_SIZE = 4096
DISPLAY_CONNECT_TIMEOUT = 10
STIMULI_HZ = [10, 15, 20, 25]

logger = logger('RemoteDisplayController')


class RemoteDisplayController():
    def __init__(self, hostname: str = None, port: int = None, local: bool = False):
        self.hostname = hostname
        self.port = port
        self.local = local

        self.current_stimuli = mp.Value('i', 0)
        self.terminate = mp.Event()
        self.lock = mp.Lock()

        self.stimulus = self.get_stimuli_list_from_BCI_controller() if not self.local else STIMULI_HZ

    def get_stimuli_list_from_BCI_controller(self):
        logger.info(f'Waiting for BCI... Be patient. Remaining: {DISPLAY_CONNECT_TIMEOUT}s')
        try:
            bci_stims = receive_through_socket((self.hostname, self.port), timeout=DISPLAY_CONNECT_TIMEOUT)
        except SocketTimeout:
            logger.warn(f"Didn't received any data from BCI-Controller. Proceeding with local configuration...")
            return STIMULI_HZ

        return bci_stims

    def start_stimuli_display(self):
        if not self.local:
            self.start_comms_listener()

        StimuliDisplay(self.stimulus, self.current_stimuli)

    def start_comms_listener(self):
        self.listener = mp.Process(name="BCIDisplayListener", target=self._comms_listener,
                               args=(self.current_stimuli,))
        self.listener.daemon = True
        self.listener.start()

    def stop_comms_listener(self):
        self.listener.terminate()

    def _comms_listener(self, shared_variable):
        state = True
        while state:
            with self.lock:
                payload = receive_through_socket((self.hostname, self.port)) #(int.from_bytes(receive_through_socket((self.hostname, self.port)), "big"))
                self.current_stimuli.value = payload


class StimuliDisplay(object):
    def __init__(self, stim_list, stim_pointer, stim_layout='default_4', calibration_mode=False):
        self.window = visual.Window(
            monitor="ExperimentScreen", units='pix', fullscr=True, color=[-1, -1, -1])

        pointer = visual.Polygon(
            self.window,
            edges=3,
            radius=50,
            pos=(0, 250),
            ori=180,
            color=[-1, 1, 1],
        )

        # This part is layout definition. You can assign custom stimuli layouts according to your needs.
        # TODO: Automatic grid template generation based on stimuli number.
        layouts = {
            'default_4': [
                visual.Rect(
                    win=self.window,
                    units="pix",
                    width=300,
                    height=300,
                    fillColor=[0, 1, 0],
                    pos=(700, 300)
                ),
                visual.Rect(
                    win=self.window,
                    units="pix",
                    width=300,
                    height=300,
                    fillColor=[1, 1, 0],
                    pos=(700, -300)
                ),
                visual.Rect(
                    win=self.window,
                    units="pix",
                    width=300,
                    height=300,
                    fillColor=[1, 1, 0],
                    pos=(-700, -300),
                ),
                visual.Rect(
                    win=self.window,
                    units="pix",
                    width=300,
                    height=300,
                    fillColor=[1, 1, 0],
                    pos=(-700, 300),
                )
            ]
        }

        self.current_frame = 0

        while True:
            for i, stim in enumerate(stim_list):
                layouts[stim_layout][i].setFillColor([-1, self._calc_frame_rate(stim), -1])
                layouts[stim_layout][i].draw()

                pointer.pos = layouts[stim_layout][stim_pointer.value].pos

                if not calibration_mode:
                    pointer.draw()
                else:
                    visual.TextStim(self.window, f'Item {i} : {stim} hz', color=(
                        0, 250, 0), pos=layouts[stim_layout][i].pos, colorSpace='rgb').draw()

            self.window.flip()
            self.current_frame += 1

            for key in event.getKeys():
                if key in ['escape', 'q']:
                    core.quit()

    def _calc_frame_rate(self, stim_freq, monitor_hz=DISPLAY_REFRESH_RATE):
        return sin(stim_freq*pi*2*self.current_frame/monitor_hz)


if __name__ == "__main__":
    display = RemoteDisplayController(DISPLAY_SOCKET_ADDRESS, DISPLAY_SOCKET_PORT)
    display.start_stimuli_display()
    while True:
        sleep(1)
    # #print(display.current_stimuli.value)