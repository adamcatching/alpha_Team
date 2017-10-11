import cPickle as pic #cPickle implements pickle in C, so it's faster
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# #Opening csv files for comparison
input_1 = sys.argv[1]
input_2 - sys.argv[2]
# #
matrix1 = np.loadtxt(input_1, delimiter=',', skiprows=1, usecols=range(1,79))
matrix2 = np.loadtxt(input_2, delimiter=',', skiprows=1, usecols=range(1,79))
print matrix1, matrix2
matrix_new =  np.subtract(matrix1,matrix2) # np.zeros((3,3)) print
print matrix_new

df = pd.DataFrame(matrix_new)
df.to_csv("differences.csv")
sns.heatmap(df,cmap="Greys_r",fmt="",linewidths=0.5) #cmap="YlGnBu", cmap="RdYlGn", cmap="viridis", annot=True,
plt.yticks(rotation=0)
plt.show()
