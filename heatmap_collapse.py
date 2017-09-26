#!/usr/bin/python
import _pickle as pic
import sys
import itertools
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

## The purpose of this script is to import and visualize the barcode library. 
## What barcodes are present, and to see if all mutations are present in the library 

data = pic.load(open("allele_dic_with_WT.pkl","rb")) # load data from pickle

print(len(data)) # tells you how many key/value pairs are in data dict
#print [(k, len(list(v))) for k, v in itertools.groupby(sorted(data.values()))] # tells you the frequency of each key/value pair in data dict
datavalues = data.values()

#print(datavalues[0], mutantdict[0])

# Read DNA to RNA
def nuc_to_codon(neuc):
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

# Input the pickles
barcode_data = pic.load(open("allele_dic_with_WT.pkl","rb"))
codons = pic.load(open("translate.pkl","rb"))
aa_value = pic.load(open("aminotonumber.pkl","rb"))

# Create numpy array that goes from 0 to 77 places
mut_per_loc = np.zeros((21,78))

# Define a function that will convert a codon to an amino acid
def codon_to_aa(codon):
    rna_codon = ''
    for nuc in codon:
        new_nuc = nuc_to_codon(nuc)
        rna_codon += new_nuc
    amino = codons[rna_codon]
    return amino

sorted_aa_value = sorted(aa_value.items(), key=lambda x: x[1])

for item in datavalues:
    if item[1] != 'WT':
        pos1 = int(item[0])
        input_codon = item[1]
        new_aa = codon_to_aa(input_codon)
        for num_aa in sorted_aa_value:
            if new_aa == num_aa[0]:
                pos2 = num_aa[1]
        mut_per_loc[pos2, pos1] += 1

# Initialize 1D array of 20s to subtract from
num_no_mut = np.ones(78) * 21
num_of_aa_mut = np.zeros(21)

# Go through the number of mutations at each location
for i, line in enumerate(mut_per_loc):
    # For every numbered location along the mutation type
    num_mut_aa = np.sum(line)
    num_of_aa_mut[i] = num_mut_aa
    for j, pos in enumerate(line):
        # If there are zero mutations at this residue at this position
        if pos == 0:
            # Subtract from the array of 20s
            num_no_mut[j] -= 1
sorted_aa = [item[0] for item in sorted_aa_value]
x = np.linspace(0, 21, 22)
print(num_of_aa_mut)
plt.plot(num_of_aa_mut,'-*',color = 'navy')
plt.xticks(x,sorted_aa)
plt.ylabel("Number of Mutations Present")
plt.title("Number of Each Mutation Type")
plt.savefig("Number_of_Each_Mutation_Type.png")
plt.show()
"""
# Plot and label
plt.plot(num_no_mut, 'o', color = 'FireBrick')
plt.ylabel('Number of Mutations')
plt.xlabel('Position Along Sequence')
plt.title('Number of Unique Mutations per Site')
plt.savefig('Unique_Mutations_per_Site.png')
plt.show()
"""
"""
plt.imshow(mut_per_loc, cmap='viridis')
plt.show()
"""
