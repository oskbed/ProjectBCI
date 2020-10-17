import asyncio
from sklearn.cross_decomposition import CCA
import numpy as np
import time


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

a = [ref(20), ref(21), ref(22)]
b = [ref(20), ref(11), ref(22)]

def correlate(reference, signal):
    for ref in range(len(reference)):
        sample = signal[0] # [:, 0:channels_num]

        cca = CCA(n_components=2)
        cca_ref = CCA(n_components=1)
        cca_all = CCA(n_components=1)

        ref_ = reference[ref]
        ref_2 = reference[ref][:, [0, 1, 4, 5]]
        ref_all = reference[ref][:, [0, 1, 2, 3, 4, 5]]

        cca.fit(sample, ref_)
        cca_ref.fit(sample, ref_2)
        cca_all.fit(sample, ref_all)

        u, v = cca.transform(sample, ref_)
        u_2, v_2 = cca_ref.transform(sample, ref_2)
        u_3, v_3 = cca_all.transform(sample, ref_all)

        corr = abs(np.corrcoef(u.T, v.T)[0, 1])
        corr2 = abs(np.corrcoef(u_2.T, v_2.T)[0, 1])
        corr_all = abs(np.corrcoef(u_3.T, v_3.T)[0, 1])
        print(corr, corr2, corr_all)

async def correlat(reference, signal):
    sample = signal[0] # [:, 0:channels_num]

    cca = CCA(n_components=1)
    cca_ref = CCA(n_components=1)
    cca_all = CCA(n_components=1)

    ref_ = reference[:, [0, 1, 2, 3]]
    ref_2 = reference[:, [0, 1, 4, 5]]
    ref_all = reference[:, [0, 1, 2, 3]]

    cca.fit(sample, ref_)
    cca_ref.fit(sample, ref_2)
    cca_all.fit(sample, ref_all)

    u, v = cca.transform(sample, ref_)
    u_2, v_2 = cca_ref.transform(sample, ref_2)
    u_3, v_3 = cca_all.transform(sample, ref_all)

    corr = abs(np.corrcoef(u.T, v.T)[0, 1])
    corr2 = abs(np.corrcoef(u_2.T, v_2.T)[0, 1])
    corr_all = abs(np.corrcoef(u_3.T, v_3.T)[0, 1])
    print(corr, corr2, corr_all)

async def corr():
    return await asyncio.gather(*[asyncio.create_task(correlat(a[0], b)), asyncio.create_task(correlat(a[1], b)), asyncio.create_task(correlat(a[2], b))])



# start_time = time()
# correlate(a,b)
# print("--- %s seconds ---" % (time() - start_time))
start_time = time()
asyncio.run(corr())
print("--- %s seconds ---" % (time() - start_time))
