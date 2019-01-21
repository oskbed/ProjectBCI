import matplotlib.pyplot as plt

dane = pd.read_csv("outputs/SUBJ1-results.csv", delimiter=',', engine='python')

plt.plot(dane.iloc[:,0])
