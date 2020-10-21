import pickle
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM, gethostname, timeout
from errors import SocketTimeout
from utils import logger
import logging
import sys
import os
from psychopy import visual, event, core
import ast
from numpy import sin, pi
logger = logger('RemoteDisplayController')

class RemoteDisplayController():
    def __init__(self, port):
        logger.info('Display Controller initialize...')
        self.listener_port = port
        self.buffer_size = 4096
        self.ip_address_slave = gethostbyname(gethostname())
        self.session_timeout = 60

        self.stimuli_freq = self._get_stims_from_main_controller()
        logger.info('Display Controller initialized sucessfully!')

    def _get_stims_from_main_controller(self):
        self.controller_socket = socket(AF_INET, SOCK_DGRAM)
        self.controller_socket.settimeout(self.session_timeout)
        self.controller_socket.bind((self.ip_address_slave, self.listener_port))

        logger.info(f"Expecting data from BCI Application. Timeout: {self.session_timeout}. "
                    f"\n Listener on port: {self.listener_port}")

        try:
            while True:
                (data, addr) = self.controller_socket.recvfrom(self.buffer_size)
                if not data == None:
                    stimulus = pickle.loads(data)
                    logger.info("Data received! Closing connection...")
                    return stimulus
        except timeout as e:
            raise SocketTimeout(f"Timeout for socket, didn't receive any data in {self.session_timeout} seconds period!")
        finally:
            self.controller_socket.close()

    def start_stimuli_display(self):
        StimuliDisplay(self.stimuli_freq)


class StimuliDisplay(object):
    def __init__(self, stims, layout='default_4'):
        self.stimuli_freq = stims
        self.selected_layout = layout
        self.window = visual.Window(
            monitor="ExperimentScreen", units='pix', fullscr=True, color=[-1, -1, -1])

        displayed_marker = visual.Polygon(
            self.window,
            edges=3,
            radius=50,
            pos=(0, 250),
            ori=180,
            color=[-1, 1, 1],
        )

        displayed_layout = {
            'default_4': {
                'upper_left': visual.Rect(
                    win=self.window,
                    units="pix",
                    width=300,
                    height=300,
                    fillColor=[0, 1, 0],
                    pos=(700, 300)
                ),
                'lower_left':  visual.Rect(
                    win=self.window,
                    units="pix",
                    width=300,
                    height=300,
                    fillColor=[1, 1, 0],
                    pos=(700, -300)
                ),
                'upper_right': visual.Rect(
                    win=self.window,
                    units="pix",
                    width=300,
                    height=300,
                    fillColor=[1, 1, 0],
                    pos=(-700, -300),
                ),
                'lower_right':   visual.Rect(
                    win=self.window,
                    units="pix",
                    width=300,
                    height=300,
                    fillColor=[1, 1, 0],
                    pos=(-700, 300),
                )
            }
        }

        self.current_frame = 0

        while True:
            for stim_index, (name, item) in enumerate(displayed_layout[self.selected_layout].items()):
                try:
                    item.setFillColor([-1, self._calc_frame_rate(self.stimuli_freq[stim_index]), -1])
                    item.draw()
                except IndexError:
                    logger.warn('This layout is not proper for number of stimuli provided. Select more adequate layout!')
                    continue

            displayed_marker.pos = displayed_layout[self.selected_layout]['upper_right'].pos
            displayed_marker.draw()
            self.window.flip()
            self.current_frame += 1

            for key in event.getKeys():
                if key in ['escape', 'q']:
                    core.quit()

    def _calc_frame_rate(self, stim_freq, monitor_hz=60):
        return sin(stim_freq*pi*2*self.current_frame/monitor_hz)


if __name__ == "__main__":
    display = RemoteDisplayController(2092)
    display.start_stimuli_display()
