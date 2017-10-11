import cPickle as pic
import sys
import itertools
import re
import subprocess
from collections import defaultdict

#### VERSION: PYTHON 2.7 | created by Yessica 10-10-17
### Takes a merged fastq and a dictionary pickle as input and outputs a single modified dictionary
### Expects the command-line arguments " python SCRIPTNAME FASTQ_FILE DICT_PICKLE "

# define wildtype aSyn nucleotide sequence
wt = 'ATGGATGTATTCATGAAAGGACTTTCAAAGGCCAAGGAGGGAGTTGTGGCTGCTGCTGAGAAAACCAAACAGGGTGTGGCAGAAGCAGCAGGAAAGACAAAAGAGGGTGTTCTCTATGTAGGCTCCAAAACCAAGGAGGGAGTGGTGCATGGTGTGGCAACAGTGGCTGAGAAGACCAAAGAGCAAGTGACAAATGTTGGAGGAGCAGTGGTGACGGGTGTGACAGCAGTAGCCCAGAAGACAGTGGAGGGAGCAGGGAGCATTGCAGCAGCCACTGGCTTTGTCAAAAAGGACCAGTTGGGCAAGAATGAAGAAGGAGCCCCACAGGAAGGAATTCTGGAAGATATGCCTGTGGATCCTGACAATGAGGCTTATGAAATGCCTTCTGAGGAAGGGTATCAAGACTACGAACCTGAAGCC'
# Import Nish's dict from pickle, plus Jenna's fastq file containing barcodes and aSyn sequences
fastq_file = sys.argv[1] # fastq file containing merged aSyn sequences with barcodes at the end
pickle2 = sys.argv[2] # main input, barcode/mutation
bcdict = pic.load(open(pickle2,"rb"))
barcodes_off = bcdict.keys() # Pull barcodes from dict into list
barcodes_act =[] # will be used below to pull barcodes from fastq file
print len(barcodes_off) # tells you size of inputs

# For each barcode, pull the corresponding location(s), and for given location(s), pull the corresponding aSyn sequence(s)
with open(fastq_file) as fp: # open the fastq file
    for each in barcodes_off: # go through all barcodes for each line
        locations = []
        print "MUTATION: %s\tBARCODE: %s" %(bcdict.get(each), each) # header for legibility
        for line in enumerate(fp): # go through each line w/o storing all in memory
            if each in line: # if this line contains the barcode
                print each, line #DEBUG
                location = line.split[-18:-1]
                print location[0] #DEBUG
                locations.append(location) # print the corresponding aSyn sequence for all matches
                # Compare the seqs and spit back cases where diff > 0
        for a, b in itertools.combinations(locations,2):
            print
                # If there are multiple instances of both possible barcodes not matching other barcodes...
                    # throw it out

# Return new dictionary
