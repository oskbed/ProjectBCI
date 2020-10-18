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
        filtered = np.zeros(shape=(self.channels, self.sampling_rate))

        for channel_id, channel_data in enumerate(data):
            for packet_id, packet in enumerate(channel_data):
                filtered[channel_id, packet_id] = self.filter.filterIIR(packet, channel_id)

        filtered = filtered.reshape(-1, self.channels)

        for n, refs in enumerate(self.method.stimuli_reference_signals):
            _norm = self.method.get_score(filtered, refs.reference_signals[0:2].reshape(-1,2))
            _harm = self.method.get_score(filtered, refs.reference_signals[2:4].reshape(-1,2))
            _sub = self.method.get_score(filtered, refs.reference_signals[4:6].reshape(-1,2))
            _all = self.method.get_score(filtered, refs.reference_signals.reshape(-1,6))
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