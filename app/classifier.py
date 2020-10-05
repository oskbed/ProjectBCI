import importlib
import os
import .cca
import enum
import .filters


class ClassifierMethods(enum.Enum):
    CCA = cca.CrossCorrelation()

class ClassifierDataFilters(enum.Enum):
    IIR = filters.OnlineIIRFilter()


class Classifier:
    def __init__(self, board=None, method=None):
        self.board = board
        self.method = self._select_method(method.upper())
        self.filter = filters.OnlineIIRFilter()

        # Internal status
        self._data_processing = False

    def _select_method(self, selected):
        return [method.value for method in ClassifierMethods if method.name == selected]



    def acquire_data(self):
        pass

    def process_data(self):
        self._data_processing = True
        data = self.board.get_current_board_data(256)
        filtered_data = 

    def filtering(self, packet):
        """ Push single sample into the list """
        for i in range(self.channels_num):
            packet[i] = self.flt.filterIIR(packet[i], i)

        return packet
class Detection:
    pass