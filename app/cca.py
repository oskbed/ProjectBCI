from reference import SignalReference
from sklearn.cross_decomposition import CCA
import numpy as np


class CrossCorrelation:
    def __init__(self):
        self.stimuli_reference_signals = []

    def get_score(self, signal, reference):
        cca = CCA(n_components=1)

        cca.fit(signal, reference)

        u, v = cca.transform(signal, reference)
        return abs(np.corrcoef(u.T, v.T)[0, 1])

    def add_reference_signal(self, hz):
        return self.stimuli_reference_signals.append(SignalReference(hz))
