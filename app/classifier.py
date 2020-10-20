import importlib
import os
import cca
import enum
import filters
import numpy as np
from utils import *

class ClassifierMethods(enum.Enum):
    CCA = cca.CrossCorrelation()

class ClassifierDataFilters(enum.Enum):
    IIR = filters.OnlineIIRFilter()


class Classifier:
    def __init__(self, board=None, method=None, flt= None):
        self.board = board
        self.method = method # self._select_method(method.upper())
        self.filter = flt # filters.OnlineIIRFilter()
        self.channels = 2
        self.sampling_rate = 256
        self.sampling_interval = 1 # second
        self.display = False

    # def _select_method(self, selected):
    #     return [method.value for method in ClassifierMethods if method.name == selected]

    @property
    def reference_signals(self):
        return self.method.stimuli_reference_signals

    def acquire_data(self):
        pass

    def process_data(self):
        scores = []
        data = np.array(self.board.get_current_board_data(self.sampling_rate))[:self.channels]
        filtered = np.zeros(shape=(self.sampling_rate, self.channels))

        for channel_id, channel_data in enumerate(data):
            for packet_id, packet in enumerate(channel_data):
                filtered[packet_id, channel_id] = self.filter.filterIIR(packet, channel_id)

        for n, refs in enumerate(self.method.stimuli_reference_signals):
            _norm = self.method.get_score(filtered, refs.signal[:, 0:2])
            _harm = self.method.get_score(filtered, refs.signal[:, 2:4])
            _sub = self.method.get_score(filtered, refs.signal[:, 4:6])
            _all = self.method.get_score(filtered, refs.signal[:, :])
            scores.append(Detection(refs.hz, _norm, _harm, _sub, _all))

        return scores


class Detection:
    def __init__(self, stimuli_hz, normal, harmonic, subharmonic, all_):
        self.stimuli_hz = stimuli_hz
        self.normal = normal
        self.harmonic = harmonic
        self.subharmonic = subharmonic
        self.all = all_

    @property
    def corr_score(self):
        return [self.normal, self.harmonic, self.subharmonic, self.all]
