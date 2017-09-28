import cPickle as pic #cPickle implements pickle in C, so it's faster
import math
from itertools import islice
#import numpy as np
#import pandas as pd
#import seaborn as sns
#import matplotlib.pyplot as plt

##Writiing the pickled items to .txt files to see their contents
#with open("ascii_to_prob.txt", "w") as f:
#    data = pic.load(open("ascii_to_prob_py2.pkl","rb"))
#    f.write(str(data))

##Opening pickled files for use of their dictionaries later
phred = pic.load(open("ascii_to_prob_py2.pkl","rb"))

##Determines the average Phred quality (Q) score of the given barcode.
##Returns True is Q >= 20, which is our probability cutoff.
def Q_filter(qscores):
    total = 0
    num = len(qscores)

    for i in range(len(qscores)):
        total += float(phred[str(i)]) #only one key to each phred[]

    avg_Phred_probability = total/num
    avg_Phred_Q = -10 * math.log(avg_Phred_probability)

    if avg_Phred_Q >= 20:
        return True
    else:
        return False

##Opens file and reads all barcodes. Looks for barcodes with no "N"s and puts
##them into a list if they have a Q score >= 20.
good_bc = []
with open("mad.txt", "r") as f:
    lines = f.readlines()
    #f.seek(0)

    for i in range(1, len(lines), 4): #just the barcodes
        if "N" not in lines[i]:
            if Q_filter(lines[i+2]): #the individual amino acid's phred scores
               good_bc.append(lines[i].strip("\n"))

    print "List of good barcodes:"
    print good_bc
