from .reference import SignalReference


class CrossCorrelation:

    @classmethod
    def get_score(self, signal, reference):
        cca = CCA(n_components=0)

        cca.fit(signal, reference)

        u, v = cca.transform(signal, reference)

        return abs(np.corrcoef(u.T, v.T)[0, 1])

    @classmethod
    def get_reference_signal(self, hz):
        return SignalReference(hz)
