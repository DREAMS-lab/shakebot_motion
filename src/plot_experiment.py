import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

# data = np.genfromtxt('/home/napster/exp0.csv', delimiter=',')
data = pd.read_csv('/home/napster/exp270.csv')
print(data.head(6))
filt_data = data[["PGV/PGA","PGA", "Rock Status"]]
# print(filt_data)

toppled = filt_data[filt_data["Rock Status"] == "Y"].drop("Rock Status", axis=1)
balanced = filt_data[filt_data["Rock Status"] == "N"].drop("Rock Status", axis=1)
print(toppled)

plt.scatter(toppled["PGA"] ,toppled["PGV/PGA"], color="red", label="Toppled")
plt.scatter(balanced["PGA"], balanced["PGV/PGA"], color="blue", label="Balanced")
plt.legend()
plt.ylabel("PGV/PGA")
plt.xlabel("PGA")
plt.show()