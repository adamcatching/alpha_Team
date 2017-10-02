import cPickle as pic
import sys
import readline
import itertools
import re
from collections import defaultdict

# Call using "python SCRIPT FAKEMUTDICT.pkl R2.fastq"

name = sys.argv[1] # mutation dict
nametwo = sys.argv[2] # barcode fastq file
keys = []
values = []
pattern = re.compile('[A-Z]{10}')
mutdict = pic.load(open(name,"rb")) # load original pickle
values = mutdict.values()

with open(nametwo,"r") as g: # barcode locations
    file = g.readlines()
    for lines in file:
        if len(lines) == 27:
            check = pattern.match(lines)
            if str(check) != "None":
                keys.append(lines.rstrip())

print len(keys), len(values)
dictionary = dict(itertools.izip(keys, values))
print len(dictionary)

pic.dump(dictionary, open( "mutdict.pkl", "wb" ) )
