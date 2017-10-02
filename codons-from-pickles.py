#!/usr/bin/python
import cPickle as pic
import sys
import itertools
from collections import defaultdict

## The purpose of this script is to import and visualize the barcode library. 
## What barcodes are present, and to see if all mutations are present in the library 

# transcription subroutine #
def transcription (string):
    newstring = ''
    newbase = ''     
    for base in string:
        if base is 'T': newbase = 'A'
        if base is 'G': newbase = 'C'
        if base is 'C': newbase = 'G' 
        if base is 'U': newbase = 'T' 
        if base is 'W': newbase = 'W' 
        newstring += newbase
    return newstring

data = pic.load(open("allele_dic_with_WT.pkl","rb")) # load data from pickle
translator = pic.load(open("translate.pkl","rb")) # the dict for turning codons into aa
print len(data) # tells you how many key/value pairs are in data dic
#print data # tells you how many key/value pairs are in data dictt
print [(k, len(list(v))) for k, v in itertools.groupby(sorted(data.values()))] # tells you the frequency of each key/value pair in data dict

position = []
aamutant = []
datavalues = data.values()
for item in datavalues: # this loop takes the keys from the prev dict and turns them into lists
    position.append(item[0]) # position does not change
    transcript = transcription(item[1]) # transcribe the string
    if transcript in translator: temp = translator[transcript]
    else: temp = '*'
    aamutant.append(temp) # translate the codon to an aa, then add to list
transldict = dict(itertools.izip(position,aamutant)) # zip these two lists into a dictionary
print len(transldict)
print transldict

