import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0.0, 1.0, 1./256)
def get_signal_plot(raw, filtered):
    print(raw.shape, filtered.shape)
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(t, raw[0], t, filtered[0])
    axs[0].set_xlim(0, 2)
    axs[0].set_xlabel('time')
    axs[0].set_ylabel('s1 and s2')
    axs[0].grid(True)

    #cxy, f = axs[1].cohere(raw, filtered, raw.shape, 1./256)
    #axs[1].set_ylabel('coherence')

    fig.tight_layout()
    plt.show()
