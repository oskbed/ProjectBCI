import asyncio
from sklearn.cross_decomposition import CCA
import numpy as np
import time
from filters import *

from functools import wraps
from time import time

def ref(hz):
    fs = 1./256
    t = np.arange(0.0, 1.0, fs)
    reference = np.zeros(shape=(len(t), 6))
    reference[:, 0] = np.array([np.sin(2*np.pi*i*hz) for i in t]) # sin
    reference[:, 1] = np.array([np.cos(2*np.pi*i*hz) for i in t]) # cos
    reference[:, 2] = np.array([np.sin(2*np.pi*i*hz*2) for i in t]) #
    reference[:, 3] = np.array([np.cos(2*np.pi*i*hz*2) for i in t]) #
    reference[:, 4] = np.array([np.sin(2*np.pi*i*hz*0.5) for i in t]) #
    reference[:, 5] = np.array([np.cos(2*np.pi*i*hz*0.5) for i in t]) #
    return reference
a = OnlineIIRFilter()



# async def corr():
#     return await asyncio.gather(*[for i in range(ref(20).shape[1])])

def filter_test(packet, channel):
    return a.filterIIR(packet, channel)


start_time = time()

# for i in ref(20):
#     for z in range(ref(20).shape[1]):
#        filter_test(i, z)
for z in range(ref(20).shape[1]):
    for i in ref(20)[:, z]:
        filter_test(i,z)
print("--- %s seconds ---" % (time() - start_time))


# start_time = time()
# asyncio.run(corr())
# print("--- %s seconds ---" % (time() - start_time))
