#!/usr/bin/venv python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-

import brainflow
from boards import DefaultBoard
from utils import logger
import sys
from filters import OnlineIIRFilter
from cca import CrossCorrelation
from classifier import Classifier
from socket import socket, gethostbyname, AF_INET, SOCK_DGRAM, gethostname, timeout
import pickle
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds

logger = logger('Controller')


# Config 
# Board_name
# Board config
# Display config 
# Controller config


class Controller():
    def __init__(self, board, classification_method, online_filter, remote_display=True):
        self.board = board
        self.classification_method = classification_method
        self.online_filter = online_filter
        self.classifier = Classifier(board=board, method=classification_method, flt=online_filter)

        if remote_display:
            self.display_comms_port = 2092
            self.buffer_size = 4096
            self.ip_address_host = gethostbyname(gethostname())

    def _send_through_socket(self, data):
        sender = socket(AF_INET, SOCK_DGRAM)
        sender.connect((self.ip_address_host, self.display_comms_port))

        pickled_data = pickle.dumps(data)
    
        sender.send(pickled_data)
        sender.close()
    
    def _receive_through_socket(self):
        pass


    def set_stimulus(self, stims: list = []):
        for stimulus in stims:
            self.classifier.method.add_reference_signal(stimulus)

    def set_stimulus_display(self, stims: list = []):
        logger.info('Establishing connection with remote display... Be patient.')
        self._send_through_socket(stims)

        #prompt = input('Is remote display ready? Y/N/A \n').lower()


    def manager(self):
        pass

    def get_current_data(self, print_stats=False):
        # From display and processed
        pass

params = BrainFlowInputParams()
board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
method = CrossCorrelation()
flt = OnlineIIRFilter()

test = Controller(board=board, classification_method=method, online_filter=flt)
test.set_stimulus([19,120,22])
test.board.prepare_session()
#test.board.start_stream()