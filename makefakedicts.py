import cPickle as pic
import sys
import readline
import itertools
import re
from collections import defaultdict

name = sys.argv[1]
keys = []
values = []
i = 0
pattern = re.compile('[A-Z]')

with open(name,"r") as f:
    file = f.readlines()
    print "Read lines!"
    for line in file:
        if "@M" == line[0:2]:
            print line.rstrip()
            keys.append(line.rstrip())
        if len(line) == 27:
#        if pattern.match(line):
            values.append(line.rstrip())

print len(keys), len(values)
dictionary = dict(itertools.izip(keys, values))
print len(dictionary)

pic.dump(dictionary, open( "dict2.pkl", "wb" ) )
