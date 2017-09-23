import cPickle as pic #cPickle implements pickle in C, so it's faster
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

## Is there a bias in the barcodes? Are there different barcodes for the same mutation?
## What's the frequency?

##Writiing the pickled items to .txt files to see their contents
#with open("allele_dic.txt", "w") as f:
#    data = pic.load(open("allele_dic_with_WT.pkl","rb"))
#    f.write(str(data))

#with open("aminotonumber.txt", "w") as f:
#    data = pic.load(open("aminotonumber.pkl","rb"))
#    f.write(str(data))

#with open("translate.txt", "w") as f:
#    data = pic.load(open("translate.pkl","rb"))
#    f.write(str(data))

##Takes a neucleotide sequence and returns the codon
def neuc_to_codon(neuc):
    codon = ""
    for i in range(len(neuc)):
        if neuc[i] == "A":
            codon += "U"
        elif neuc[i] == "T":
            codon += "A"
        elif neuc[i] == "C":
            codon += "G"
        elif neuc[i] == "G":
            codon += "C"
    return codon

##Opening pickled files for use of their dictionaries later
barcode_data = pic.load(open("allele_dic_with_WT.pkl","rb"))
codons = pic.load(open("translate.pkl","rb"))
aa_value = pic.load(open("aminotonumber.pkl","rb"))

##Orders the dict by first value, which is position number
##Returns it as a tuple with [0] as the key and [1] as a tuple of [0] the position and [1] the codon
##E.g. sorted_barcode_data[0] == ('TGTCTATGTTATATCGCG', (0, 'WT'))
##E.g. sorted_barcode_data[0][1] == (0, 'WT'); sorted_barcode_data[0][1][0] == 0
sorted_barcode_data = sorted(barcode_data.items(), key=lambda x: x[1])
print sorted_barcode_data[0][1]

##Matrix y: aa # (0-20, bc includes STOP) by x: position # (0-77)
##matrix[down, aa][over, position]
matrix = [[0]*78 for i in range(21)]

##Reads the position and neuc seq of each dict entry. Calls neuc_to_codon and transfers codon to
##the codons dict to find the a.a. Then transfers the a.a. to aa_value to translate it to a number.
##That number is the specific index number of that aa in the matrix.
##E.g. 'STOP': 0 in aa_value puts info for the STOP codon frequency into matrix[0]
num_WT = 0
for i in range(0, len(sorted_barcode_data)):
    if str(sorted_barcode_data[i][1][1]) == "WT":
        num_WT += 1
    else:
        matrix[aa_value[codons[neuc_to_codon(str(sorted_barcode_data[i][1][1]))]]][sorted_barcode_data[i][1][0]] += 1

##Prints matrix
#for aa_value in range(len(matrix)):
#    print matrix[aa_value]

##Prints number of WT barcodes
print "There are", num_WT, "WT barcodes"

##Sorts aminotonumber dict by number for use as left axis
sorted_aa_value = sorted(aa_value.items(), key=lambda x: x[1])
#print sorted_aa_value

##Writes the left axis column: the keys (amino acid) of the above sorted dict
left_axis = []
for key, value in sorted_aa_value:
    left_axis.append(key)
#print left_axis

##Converts amino acid by position number matrix to a csv file for use by seaborn
df = pd.DataFrame(matrix)
df.to_csv("aabyposmatrix.csv")

##Read the csv that contains the matrix
df =  pd.read_csv("aabyposmatrix.csv")
print df.head()

##Makes a heatmap from the amino acid by position matrix csv file
sns.heatmap(df,cmap="YlGnBu",fmt="",linewidths=0.5,yticklabels=left_axis) #cmap="RdYlGn", cmap="YlGnBu", cmap="viridis", annot=True,
plt.yticks(rotation=0)
plt.show()
