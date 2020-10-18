#!/usr/bin/venv python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-

import brainflow
from boards import DefaultBoard

import logging
import sys
from filters import OnlineIIRFilter
from cca import CrossCorrelation
from classifier import Classifier


file_handler = logging.FileHandler(filename='tmp.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [stdout_handler] # file_handler

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(name)s %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('Controller')


# Config 
# Board_name
# Board config
# Display config 
# Controller config


class Controller():
    def __init__(self, board, classification_method, online_filter):
        self.board = board
        self.classification_method = classification_method
        self.online_filter = online_filter
        self.classifier = Classifier(board=board, method=classification_method, flt=online_filter)

    def set_stimulus(self, stims: list = []):
        for stimulus in stims:
            self.classifier.method.add_reference_signal(stimulus)

    def set_stimulus_display(self):
        pass

    def manager(self):
        pass

    def get_current_data(self, print_stats=False):
        # From display and processed
        pass


board = DefaultBoard({}.get('board_config', {}))
method = CrossCorrelation()
flt = OnlineIIRFilter()

test = Controller(board=board, classification_method=method, online_filter=flt)
test.set_stimulus([19,120,22])
test.board.establish_session()
test.board.start_streaming()