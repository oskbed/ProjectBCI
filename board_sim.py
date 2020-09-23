import os
import time

import pandas as pd

''' OpenBCI Ganglion Simulator '''

''' EXAMPLE: '''
'''
def handle_sample(sample):
    print(sample.channel_data)

board_sim = OpenBCISimulator("/home/.../.../SUBJ1/SSVEP_8Hz_Trial3_SUBJ1.csv")
board_sim.start_streaming(handle_sample)
'''


class OpenBCISimulator(object):
    ''' Class simulates board streaming with offline data. '''
    def __init__(self, channels=2, sample_rate=250, sim_mode=False, data_path=''):
        self.sample_rate = sample_rate
        self.channels = channels
        self.subj = 1
        self.sim_mode = sim_mode
        self.data_path = data_path or os.path.join(os.getcwd(), "outputs")
        self.data = pd.read_csv(os.path.join(self.data_path, f"SUBJ{self.subj}-signal_raw.csv"), engine='python')

    def start_streaming(self, callback):
        for counter, values in enumerate(self.data.values):
            sample = OpenBCISample(counter, values[: self.channels])
            if self.sim_mode:
                time.sleep(1./self.sample_rate)
            callback(sample)


class OpenBCISample(object):
    """Object encapulsating a single sample from the OpenBCI board."""
    def __init__(self, packet_id, channel_data):
        self.id = packet_id
        self.channel_data = channel_data

if __name__ == "__main__":
    def handle_sample(sample):
        print(sample.channel_data)

    board_sim = OpenBCISimulator()
    board_sim.start_streaming(handle_sample)
