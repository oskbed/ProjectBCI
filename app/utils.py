import numpy as np
import matplotlib.pyplot as plt
import time
import logging
import sys

def get_signal_plot(raw, filtered):
    t = np.arange(0.0, 1.0, 1./256)
    print(raw.shape, filtered.shape)
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(t, raw[0], t, filtered[0])
    axs[0].set_xlim(0, 2)
    axs[0].set_xlabel('time')
    axs[0].set_ylabel('s1 and s2')
    axs[0].grid(True)

    # cxy, f = axs[1].cohere(raw, filtered, raw.shape, 1./256)
    # axs[1].set_ylabel('coherence')

    fig.tight_layout()
    plt.show()

def logger(logger_name, logger_file='diagnostics.log', logger_level=logging.DEBUG):
    file_handler = logging.FileHandler(filename=logger_file)
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [stdout_handler, file_handler]

    logging.basicConfig(
        level=logger_level,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(name)s %(levelname)s - %(message)s',
        handlers=handlers
    )

    return logging.getLogger(logger_name)
