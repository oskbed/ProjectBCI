#!/usr/bin/venv python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-

import sys

import brainflow
from brainflow.board_shim import (BoardIds, BoardShim, BrainFlowInputParams,
                                  LogLevels)

from socket import gethostbyname, gethostname
from boards import DefaultBoard
from cca import CrossCorrelation
from classifier import Classifier
from filters import OnlineIIRFilter
from utils import logger, send_through_socket

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
        self.remote_display = remote_display
        self.classifier = Classifier(board=board, method=classification_method, flt=online_filter)

        if self.remote_display:
            # By default, the same computer. Format IP, PORT
            self.display_address = gethostbyname(gethostname()), 2092

    def set_stimulus(self, stims: list = []):
        for stimulus in stims:
            self.classifier.method.add_reference_signal(stimulus)

    def set_stimulus_on_display(self, stims: list = []):
        logger.info('Establishing connection with remote display... Be patient.')
        send_through_socket(self.display_address, stims)

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
