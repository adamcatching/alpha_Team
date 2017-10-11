import cPickle as pic #cPickle implements pickle in C, so it's faster
import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

## Looking at the timepoint matrices and comparing them
## Are there significant differences between replicates?

##Takes a neucleotide sequence and returns the codon (JIC)
# def neuc_to_codon(neuc):
#     codon = ""
#     for i in range(len(neuc)):
#         if neuc[i] == "A":
#             codon += "U"
#         elif neuc[i] == "T":
#             codon += "A"
#         elif neuc[i] == "C":
#             codon += "G"
#         elif neuc[i] == "G":
#             codon += "C"
#     return codon

# #Opening csv files for comparison
input_1 = sys.argv[1]
input_2 - sys.argv[2]
##Read the csv's that contains the matrix
df_1 = np.loadtxt(input_1, delimiter=',', skiprows=1, usecols=range(1,79))
df_2 = np.loadtxt(input_2, delimiter=',', skiprows=1, usecols=range(1,79))
print df_1, df_2

# #Make a matrix to hold the diff values
matrix = [[0]*78 for i in range(21)]
# #Subtract matrices one-to-one
matrix_new = numpy.Subtract(df_1,df_2,out=ndarray)

# #Writes the left axis column: the keys (amino acid) of the sorted dict below
left_axis = []
barcode_data = pic.load(open("allele_dic_with_WT.pkl","rb"))
sorted_barcode_data = sorted(barcode_data.items(), key=lambda x: x[1])
print sorted_barcode_data[0][1]
num_WT = 0
for i in range(0, len(sorted_barcode_data)):
    if str(sorted_barcode_data[i][1][1]) == "WT":
        num_WT += 1
    else:
        matrix[aa_value[codons[neuc_to_codon(str(sorted_barcode_data[i][1][1]))]]][sorted_barcode_data[i][1][0]] += 1
##Sorts aminotonumber dict by number for use as left axis
sorted_aa_value = sorted(aa_value.items(), key=lambda x: x[1])
for key, value in sorted_aa_value:
    left_axis.append(key)

##Converts amino acid by position number matrix to a csv file for use by seaborn
df = pd.DataFrame(matrix)
df.to_csv("differences.csv")

## Make a colorscheme for the heatmap
# my_cmap = sns.cubehelix_palette(n_colors=6, start=0, rot=0.6, gamma=1.0, hue=0.8, light=0.9, dark=0.1, reverse=True, as_cmap=True)
# #Makes a heatmap from the amino acid by position matrix csv file
sns.heatmap(df,cmap="Greys_r",fmt="",linewidths=0.5,yticklabels=left_axis) #cmap="YlGnBu", cmap="RdYlGn", cmap="viridis", annot=True,
plt.yticks(rotation=0)
plt.show()
