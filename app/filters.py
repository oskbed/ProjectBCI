import numpy as np

class OnlineIIRFilter(object):
    def __init__(self):
        self.prev_x = np.zeros((8, 5))
        self.prev_y = np.zeros((8, 5))
        self.prev_x2 = np.zeros((8, 5))
        self.prev_y2 = np.zeros((8, 5))

    def filterIIR(self, data, nrk):

        b = np.array([
                0.1750876436721012,
                0,
                -0.3501752873442023,
                0,
                0.1750876436721012
            ])
        a = np.array([
                1,
                -2.299055356038497,
                1.967497759984450,
                -0.8748055564494800,
                0.2196539839136946
            ])

        # 50 hz 
        b2 = np.array([
            0.96508099,
            -1.19328255,
            2.29902305,
            -1.19328255,
            0.96508099
        ])

        a2 = np.array([
            1,
            -1.21449347931898,
            2.29780334191380,
            -1.17207162934772,
            0.931381682126902
        ])

        j = 5 - 1
        while j > 0:
            self.prev_x[nrk, j] = self.prev_x[nrk, j - 1]
            self.prev_y[nrk, j] = self.prev_y[nrk, j - 1]
            self.prev_x2[nrk, j] = self.prev_x2[nrk, j - 1]
            self.prev_y2[nrk, j] = self.prev_y2[nrk, j - 1]
            j -= 1

        self.prev_x[nrk, 0] = data

        filtered = self.filter_data(b2, a2, b, a, nrk)
        return filtered

    def filter_data(self, b2, a2, b, a, nrk):
        value = 0.0
        for j in range(5):
            value += b2[j] * self.prev_x[nrk, j]
            if j > 0:
                value -= a2[j] * self.prev_y[nrk, j]
        self.prev_y[nrk, 0] = value
        self.prev_x2[nrk, 0] = value
        value = 0.0
        for j in range(5):
            value += b[j] * self.prev_x2[nrk, j]
            if j > 0:
                value -= a[j] * self.prev_y2[nrk, j]
        self.prev_y2[nrk, 0] = value
        return value