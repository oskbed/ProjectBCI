import sys
OpenBCI_PATH = '/home/oskar/github/NewBCI/OpenBCI_Python/'

# // Load OpenBCI_Python to $PATH variable. //
sys.path.insert(0, OpenBCI_PATH)

from sklearn.cross_decomposition import CCA
import numpy as np
import multiprocessing as mp
import openbci.cyton as bci

def handle_sample(sample):
  print(sample.channel_data[:4])

board = bci.OpenBCICyton(port='/dev/ttyUSB0')
board.print_register_settings()
board.getNbEEGChannels()
type(board.getSampleRate())

board.start_streaming(handle_sample)


class chleb(object):
    def __init__(self):
        self.status = 'chuj'
    def chuka(self):
        self.chelb = joka(self.status)
        return self.chelb


    class joka(object):
        def __init__(self):
            joka.cola = 'coca-cola'


test = chleb()

test.chuka.cola

test.chuka

kola = [1,2,3,4,5]
kola[-3:]
