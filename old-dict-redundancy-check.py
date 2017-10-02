import cPickle as pic
import sys
import subprocess
import readline
from collections import defaultdict
## VERSION:: PYTHON 2.7 | created by Yessica 09-27-17 ##
## This script takes a dictionary pickle as input and outputs a modified dictionary
## It expects the dictionary as a command-line argument "python SCRIPTNAME PICKLE"

# defining the wild-type nucleotide sequence
wt = 'ATGGATGTATTCATGAAAGGACTTTCAAAGGCCAAGGAGGGAGTTGTGGCTGCTGCTGAGAAAACCAAACAGGGTGTGGCAGAAGCAGCAGGAAAGACAAAAGAGGGTGTTCTCTATGTAGGCTCCAAAACCAAGGAGGGAGTGGTGCATGGTGTGGCAACAGTGGCTGAGAAGACCAAAGAGCAAGTGACAAATGTTGGAGGAGCAGTGGTGACGGGTGTGACAGCAGTAGCCCAGAAGACAGTGGAGGGAGCAGGGAGCATTGCAGCAGCCACTGGCTTTGTCAAAAAGGACCAGTTGGGCAAGAATGAAGAAGGAGCCCCACAGGAAGGAATTCTGGAAGATATGCCTGTGGATCCTGACAATGAGGCTTATGAAATGCCTTCTGAGGAAGGGTATCAAGACTACGAACCTGAAGCC'

# Import and load dict from pickle
pickle1 = sys.argv[1] # main script input
mutdict = pic.load(open(pickle1,"rb")) # load pickle
print len(mutdict) # tells you size of dic
#print [(k, len(list(v))) for k, v in itertools.groupby(sorted(mutdict.values()))] # tells you the frequency of each key/value pair
barcodes = mutdict.keys() # Pull barcodes from dict into list
# Import Adam's file containing overlapped aSyn sequences and barcodes (with phred scores)
data1 = sys.argv[2]

# For each barcode, locate in the file and pull all the corresponding aSyn sequence (two copies to account for overlap)
for each in barcodes:
    asynseq = []
    rawout = subprocess.check_output(["grep","%s %s" %(each,data1)])
    print rawout # DEBUG
    location = rawout.split(wt[-10:-1])
    print location # DEBUG
    asynseq.append(location[0])
    print len(asynseq), "\n"
    # Compare the seqs and spit back cases where diff > 0

    # If there are multiple instances of both possible barcodes not matching other barcodes...

    # For barcodes that map to mutations in one case, but WT in others, make sure the mutation is not in a missing section
