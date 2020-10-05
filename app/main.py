#!/usr/bin/venv python -W ignore::DeprecationWarning
# -*- coding: utf-8 -*-

import brainflow
from .boards import DefaultBoard

import logging
import sys

file_handler = logging.FileHandler(filename='tmp.log')
stdout_handler = logging.StreamHandler(sys.stdout)
handlers = [stdout_handler] # file_handler

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] {%(filename)s:%(lineno)d} %(name)s %(levelname)s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('Controller')

Board(config.get('board_config', {}))

# Config 
# Board_name
# Board config
# Display config 
# Controller config


class Controller():
    def __init__(self, board, classification_method, config: dict = {}):
        self.board = board
        self.classifier = classification_method
        self.config = config

    def set_stimulus(self, stims: list = []):
        self.config = 'sample time'
        for stimulus in stims:
            self.classifier.add_stimuli(stimulus)

    def set_stimulus_display(self):
        pass

    def manager(self):
        pass

    def get_current_data(self, print_stats=False):
        # From display and processed
        pass