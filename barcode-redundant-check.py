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
print len(fastq_file),len(bcdict),len(barcodes_off) # tells you size of inputs

## pull out all the barcodes from the fastq
# pattern = re.compile('[A-Z]{18}') # check for correct lines using re
# with open(fastq_file) as fp:
#     for line in enumerate(fp):
#         check = pattern.match(line)
#         if str(check) != "None":
#             rawbc = line[-18:-1]
#             barcodes_act.append(rawbc)
# print len(barcodes_act), barcodes_act

# For each barcode, pull the corresponding location(s), and for given location(s), pull the corresponding aSyn sequence(s)
for each in barcodes_off:
    print "MUTATION: %s\tBARCODE: %s" %(bcdict.get(each), each) # header for legibility
    locations = []
    rawout = subprocess.check_output(["grep","%s %s" %(each,fastq_file)]) # grep the fastq file for the barcode seq
    print rawout # DEBUG
    loc = rawout.split(wt[-18:-1])
    print loc # DEBUG
    locations.append(loc) # all the locations that match the current barcode
    print "%s possible sequences.\n" %(len(locations))
    # Compare the seqs and spit back cases where diff > 0
    # for a, b in itertools.combinations(asynseq,2):
    #     print
    # If there are multiple instances of both possible barcodes not matching other barcodes...

    # For barcodes that map to mutations in one case, but WT in others, make sure the mutation is not in a missing section
