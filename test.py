import pandas as pd
import time
''' OpenBCI Ganglion Simulator '''

''' EXAMPLE: '''
'''
def handle_sample(sample):
    print(sample.channel_data)

CHANNELS = [1,2,3,4]

board_sim = OpenBCISimulator("/home/.../.../SUBJ1/SSVEP_8Hz_Trial3_SUBJ1.csv",
CHANNELS)
board_sim.start_streaming(handle_sample)
'''


class OpenBCISimulator(object):
    """OpenBCI Ganglion simulator class. Generate sample object from eeg file,
    and pass it further by callback function.

    Parameters
    ----------
    path : string
        Path of your eeg data set. e.g "/home/SUBJ1/SSVEP_8Hz_Trial3_SUBJ1.csv"
    channels : list
        Selected channels for generator. Min. 1 Max. 4 channels.
    sample_rate : integer
        Sampling rate, default for Ganglion 250.
    test : boolean
        If true, all samples will be parse instantly, without simulating
        sample rate time.
    """

    def __init__(self, channels, sample_rate=250, subj=0):
        self.sample_rate = sample_rate
        self.channels = channels
        self.subj = subj
        self.path = pd.read_csv(str("/Users/oskar.bedychaj/University/ProjectBCI/outputs/SUBJ" + str(self.subj) + "-signal_raw.csv"),
                                engine='python')
        self.path = self.path.iloc[:, self.channels]

    def start_streaming(self, callback):
        __temp = []
        for i in range(len(self.path)):
            for j in self.path.ix[i]:
                __temp.append(j)
            sample = OpenBCISample(i, __temp)
            __temp = []
            #if not self.test:
            #    time.sleep(1./self.sample_rate)
            callback(sample)


class OpenBCISample(object):
    """Object encapulsating a single sample from the OpenBCI board."""
    def __init__(self, packet_id, channel_data):
        self.id = packet_id
        self.channel_data = channel_data
