import cPickle as pic
import sys
import subprocess
import readline
import itertools
from collections import defaultdict
## VERSION: PYTHON 2.7 | created by Yessica 09-27-17 ##
## Takes three dictionary pickles as input and outputs a single modified dictionary
## Expects the dictionaries as command-line arguments "python SCRIPTNAME MPICKLE BPICKLE APICKLE"

# define wildtype aSyn nucleotide sequence
wt = 'ATGGATGTATTCATGAAAGGACTTTCAAAGGCCAAGGAGGGAGTTGTGGCTGCTGCTGAGAAAACCAAACAGGGTGTGGCAGAAGCAGCAGGAAAGACAAAAGAGGGTGTTCTCTATGTAGGCTCCAAAACCAAGGAGGGAGTGGTGCATGGTGTGGCAACAGTGGCTGAGAAGACCAAAGAGCAAGTGACAAATGTTGGAGGAGCAGTGGTGACGGGTGTGACAGCAGTAGCCCAGAAGACAGTGGAGGGAGCAGGGAGCATTGCAGCAGCCACTGGCTTTGTCAAAAAGGACCAGTTGGGCAAGAATGAAGAAGGAGCCCCACAGGAAGGAATTCTGGAAGATATGCCTGTGGATCCTGACAATGAGGCTTATGAAATGCCTTCTGAGGAAGGGTATCAAGACTACGAACCTGAAGCC'

# Import and load Nish's dict from pickle, plus Jenna's dicts containing barcodes and aSyn sequences separately
pickle1 = sys.argv[1] # main input, barcode/mutation
mutdict = pic.load(open(pickle1,"rb")) # load pickle
pickle2 = sys.argv[2] # barcode/location
bcdict = pic.load(open(pickle2,"rb"))
pickle3 = sys.argv[3] # aSyn/location
asdict = pic.load(open(pickle3,"rb"))
print len(mutdict),len(bcdict),len(asdict) # tells you size of dicts
#print [(k, len(list(v))) for k, v in itertools.groupby(sorted(mutdict.values()))] # tells you the frequency of each key/value pair
barcodes = mutdict.keys() # Pull barcodes from mutdict into list

# For each barcode, pull the corresponding location(s), and for given location(s), pull the corresponding aSyn sequence(s)
for each in barcodes:
    print "MUTATION: %s\tBARCODE: %s" %(mutdict.get(each), each)
    locations = []
    asynseq = []
    for location, bc in bcdict.items():
        if bc == each:
            locations.append(location) # all the locations that match the current barcode in BPICKLE
    for possibles in locations: # which locations return an aSyn sequence in the APICKLE
        if possibles in asdict:
            asynseq.append(asdict.get(possibles)) # append the sequences to a list (should = # of locations)
    print "%s possible locations returned %s sequences.\n" %(len(locations), len(asynseq)), asynseq
    # Compare the seqs and spit back cases where diff > 0
    # for a, b in itertools.combinations(asynseq,2):
    #     print
    # If there are multiple instances of both possible barcodes not matching other barcodes...

    # For barcodes that map to mutations in one case, but WT in others, make sure the mutation is not in a missing section
