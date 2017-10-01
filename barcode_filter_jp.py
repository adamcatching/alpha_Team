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
        total += float(phred[str(qscores[i])]) #only one key to each phred[]

    avg_Phred_probability = total/num
    avg_Phred_Q = -10 * math.log(avg_Phred_probability)

    if avg_Phred_Q >= 20:
        return True
    else:
        return False

##Takes the line that only has the overlapping part in R3. Returns the start and
##stop indices of the overlap.
def get_overlap(seq):
    start = 0
    stop = 0
    got_start = False
    got_stop = False

    while not got_stop:
        for i in range(len(seq)):
            if seq[i] != " " and not got_start:
                start = i
                got_start = True
            if seq[i] == " " and got_start:
                stop = i - 1
                got_stop = True
                break
    return start, stop

##Takes R1, R3, and the phred scores for their individual nucleotides (phR1 and phR3).
##Compares the phred scores of each nucleotide in the overlap. Selects the nucleotide
##that has the lower phred score (less uncertainty) as the nucleotide in the "correct"
##a-syn overlap seq, the "good overlap". Returns the good overlap.
def compare_overlaps(R1, R3, phR1, phR3):
    good_overlap = ""
    for i in range(len(R1)): #all same length anyway
        if phred[phR1[1]] < phred[phR1[2]]:
            good_overlap += R1[i]
        elif phred[phR1[1]] > phred[phR1[2]]:
            good_overlap += R3[i]
        elif phred[phR1[1]] == phred[phR1[2]] and R1[i] != R3[i]:
            good_overlap += "?"
        elif phred[phR1[1]] == phred[phR1[2]] and R1[i] == R3[i]:
            good_overlap += R1[i]
    return good_overlap

##Replaces the nucleotides in the overlap of R1 with the nucleotides of the "correct", good overlap seq.
def paste_seqs((start, stop), R1, good_overlap):
    good_seq = R1[0:start] + good_overlap + R1[stop:]
    return good_seq

##Opens file and reads all barcodes. Looks for barcodes with no "N"s and puts
##them into a list if they have a Q score >= 20.
good_bc = []
#with open("sad.txt", "r") as f:
with open("Composite_toy.fastq", "r") as f:
    lines = f.readlines()
    #f.seek(0)
    print str.rstrip(lines[1])
    #print lines[1][:446]

    barcodes = {}
    merged_asyn = {}
    for i in range(1, len(lines), 6): #just the barcodes
        #print lines[i][-26:-1]
        if "N" not in lines[i][-27:-1]:
            if Q_filter(lines[i+3][-27:-1]) == True: #the individual amino acid's phred scores
                (start, stop) = get_overlap(lines[i+1])
                good_overlap = compare_overlaps(lines[i][start:stop], lines[i+1][start:stop], lines[i+3][start:stop], lines[i+4][start:stop])
                good_seq = paste_seqs((start, stop), str.rstrip(lines[i]), good_overlap)
                #print "yes", good_seq
                good_bc.append(lines[i][-27:-1])
                barcodes[str.rstrip(lines[i-1])] = lines[i][-27:-1]
                merged_asyn[str.rstrip(lines[i-1])] = good_seq[:-27]

    print "List of good barcodes:"
    print good_bc

    print barcodes
    print merged_asyn
