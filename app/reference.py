import numpy as np


class SignalReference(object):
    """ Reference Signals"""
    def __init__(self, hz, sampling_rate=256, mod_list=[1, 2, 0.5]):

        self.hz = hz

        __t_arr = np.arange(0.0, 1.0, 1./sampling_rate)

        self.signal = np.zeros(shape=(len(__t_arr), len(mod_list)*2))

        references = []

        for modifier in mod_list:
            references.append(np.array([np.sin(2*np.pi*i*self.hz*modifier) for i in __t_arr]))
            references.append(np.array([np.cos(2*np.pi*i*self.hz*modifier) for i in __t_arr]))

        for channel, ref in enumerate(references):
            self.signal[:, channel] = ref
