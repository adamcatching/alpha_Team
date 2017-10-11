import cPickle as pic
import sys
import readline
import itertools
import re
from collections import defaultdict

# ' python SCRIPT FASTQ_FILE MUTDICT_PICKLE '

name = sys.argv[1]
key = []
value = []
i = 0
pattern = re.compile('[A-Z]{125}')

with open(name,"r") as f:
    file = f.readlines()
    print "Read lines!"
    for line in file:
        # if "@M" == line[0:2]:
        #     print line.rstrip()
        #     keys.append(line.rstrip())
#        if len(line) == 27:
        if pattern.match(line):
            line = line.rstrip()
            key.append(line[-18:-1])

pickle2 = sys.argv[2] # barcode/mutation
bcdict = pic.load(open(pickle2,"rb"))
value = bcdict.values() # Pull barcodes from dict into list

print "Keys\tValues"
print "%s\t%s\n" %(len(key), len(value))
dictionary = dict(itertools.izip(key, value))
print len(dictionary)
pic.dump(dictionary, open( "dict2.pkl", "wb" ) )
