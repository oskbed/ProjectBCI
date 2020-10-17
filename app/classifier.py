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

        # Internal status
        self._data_processing = False

    # def _select_method(self, selected):
    #     return [method.value for method in ClassifierMethods if method.name == selected]

    @property
    def reference_signals(self):
        return self.method.stimuli_reference_signals

    def acquire_data(self):
        pass

    def process_data(self):
        self._data_processing = True
        data = np.array(self.board.get_current_board_data(256))[:4]
        filtered = np.zeros(shape=(data.shape[0], data.shape[1]))
        print(data.shape, filtered.shape)
        #FIX SHAPES

        for channel_id, channel_data in enumerate(data):
            for packet_id, packet in enumerate(channel_data):
                filtered[channel_id, packet_id] = self.filter.filterIIR(packet, channel_id)

        # Working #
        # for channel_id in enumerate(data.shape[0]):
        #     for packet_id, packet in enumerate(data[channel_id, :]):
        #         filtered[channel_id, packet_id] = self.filter.filterIIR(packet, channel_id)
        get_signal_plot(data,filtered)
        return data, filtered
        ####
        #for channel_id in data::
            # for sample_id, sample in data[:, channel_id]:
            #     filtered[sample_id, channel_id] = self.filter.filterIIR(sample[channel_id], channel_id)

        # for ref_signal in self.reference_signals:
        #     print(self.method.get_score(filtered, ref_signal), ref_signal.hz)

        # return filtered


class Detection:
    pass