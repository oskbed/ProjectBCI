import numpy as np
import matplotlib.pyplot as plt
import time
import logging
import sys
from socket import (AF_INET, SOCK_DGRAM, gethostbyname, gethostname, socket,
                    timeout)
import pickle


class SocketTimeout(BaseException):
    '''Exception raised in case listener do not receive any data in time.'''
    pass


LOG_FILENAME = 'system.log'


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


def logger(logger_name, logger_file=LOG_FILENAME, logger_level=logging.DEBUG):
    file_handler = logging.FileHandler(filename=logger_file)
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [stdout_handler, file_handler]

    logging.basicConfig(
        level=logger_level,
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(name)s %(levelname)s - %(message)s',
        handlers=handlers
    )

    return logging.getLogger(logger_name)


def send_through_socket(address: tuple, payload, buffer_size=4096, sustainable=False):
    sender = socket(AF_INET, SOCK_DGRAM)
    sender.connect((address))

    pickled_data = pickle.dumps(payload)
    sender.send(pickled_data)
    if not sustainable:
        sender.close()


def receive_through_socket(address: tuple, buffer_size=4096, timeout=None):
    receiver = socket(AF_INET, SOCK_DGRAM)
    receiver.settimeout(timeout)
    receiver.bind((address))

    try:
        while True:
            (data, addr) = receiver.recvfrom(buffer_size)
            if data is not None:
                return pickle.loads(data)
    except Exception as e:
        raise SocketTimeout(f"Socket timeout! Didn't receive any data in defined {timeout} seconds timeout!")
    finally:
        receiver.close()
