import sys
import re
from collections import defaultdict
from collections import Counter

#### VERSION: PYTHON 2.7 | created by Yessica 10-11-17
### Counts barcodes in fastq file
### Expects the command-line arguments " python SCRIPTNAME FASTQ_FILE "

# Import fastq file containing barcodes and aSyn sequences
fastq_file = sys.argv[1] # fastq file containing merged aSyn sequences with barcodes at the end
with open(fastq_file) as fp: # open the fastq file
   locations = []
   pattern = re.compile('[A-Z]{125}')
   for line in enumerate(fp): # go through each line w/o storing all in memory
       sequence = str(line)
       if sequence.match(line):
           location = sequence[-18:-1].rstrip()
           print location #DEBUG
           locations.append(location) # print the corresponding aSyn sequence for all matches
   Counter(locations)
