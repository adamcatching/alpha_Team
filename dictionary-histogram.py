import numpy as np
import sys
import cPickle as pic


a = sys.argv[1] # this is the dictionary
myDictionary = pic.load(open(a,"rb"))

plt.bar(myDictionary.keys(), myDictionary.values(), width, color='g')
plt.hist(myDictionary)
plt.show()
