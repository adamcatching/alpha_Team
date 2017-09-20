#!/usr/bin/python
import cPickle as pic
import sys

## The purpose of this script is to import and visualize the barcode library. 
## What barcodes are present, and how many of them represent overlapping codons?
## How frequently?

data = pic.load(open("allele_dic.pkl","rb"))
print data

