import numpy as np


class SignalReference(object):
    """ Reference Signals"""
    def __init__(self, hz, sampling_rate=256, mod_list=[1, 2, 0.5]):

        self.hz = hz

        __t = np.arange(0.0, 1.0, 1./sampling_rate)

        self.reference_signals = np.zeros(shape=(len(__t), len(mod_list)*2))

        __references = []

        for modifier in mod_list:
            __references.append(np.array([np.sin(2*np.pi*i*self.hz*modifier) for i in __t]))
            __references.append(np.array([np.cos(2*np.pi*i*self.hz*modifier) for i in __t]))

        for i, ref in enumerate(__references):
            self.reference_signals[:, i] = ref
