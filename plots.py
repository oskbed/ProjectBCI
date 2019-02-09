import matplotlib.pyplot as plt
import pandas as pd
dane = pd.read_csv("outputs/SUBJ5-results.csv", delimiter=',', engine='python')


bodziec_1 = []
bodziec_2 = []
bodziec_3 = []


for i,j in enumerate(dane.iloc[2:,2]):
    if i % 3 == 0:
        bodziec_1.append(j)
    elif i % 3 == 1:
        bodziec_2.append(j)
    elif i % 3 == 2:
        bodziec_3.append(j)



len(bodziec_3)

plt.plot(bodziec_1, label="8hz")
plt.plot(bodziec_2, label="12hz")
plt.plot(bodziec_3, label="14hz")
plt.legend()
plt.title("FLT2/30 | SH |")
plt.savefig('230SH.png')
