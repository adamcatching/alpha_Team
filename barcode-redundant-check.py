import cPickle as pic
import sys
import subprocess
import readline
import itertools
from collections import defaultdict

#### VERSION: PYTHON 2.7 | created by Yessica 10-10-17
### Takes a merged fastq and a dictionary pickle as input and outputs a single modified dictionary
### Expects the command-line arguments " python SCRIPTNAME FASTQ_FILE DICT_PICKLE "

# define wildtype aSyn nucleotide sequence
wt = 'ATGGATGTATTCATGAAAGGACTTTCAAAGGCCAAGGAGGGAGTTGTGGCTGCTGCTGAGAAAACCAAACAGGGTGTGGCAGAAGCAGCAGGAAAGACAAAAGAGGGTGTTCTCTATGTAGGCTCCAAAACCAAGGAGGGAGTGGTGCATGGTGTGGCAACAGTGGCTGAGAAGACCAAAGAGCAAGTGACAAATGTTGGAGGAGCAGTGGTGACGGGTGTGACAGCAGTAGCCCAGAAGACAGTGGAGGGAGCAGGGAGCATTGCAGCAGCCACTGGCTTTGTCAAAAAGGACCAGTTGGGCAAGAATGAAGAAGGAGCCCCACAGGAAGGAATTCTGGAAGATATGCCTGTGGATCCTGACAATGAGGCTTATGAAATGCCTTCTGAGGAAGGGTATCAAGACTACGAACCTGAAGCC'

# Import and load Nish's dict from pickle, plus Jenna's dicts containing barcodes and aSyn sequences separately
fastq_file = sys.argv[1] # fastq file containing merged aSyn sequences with barcodes at the end
pickle2 = sys.argv[2] # main input, barcode/mutation
bcdict = pic.load(open(pickle2,"rb"))
barcodes = bcdict.keys() # Pull barcodes from dict into list
print len(fastq_file),len(bcdict),len(barcodes) # tells you size of inputs
