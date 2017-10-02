# merge_files.py
# Adam Catching

# Import packages
import numpy as np
import _pickle as pkl

# Define the files to open
R1 = 'R1.fastq'
R2 = 'R2.fastq'
R3 = 'R3.fastq'

# Open the file
r2 = open(R2, 'r')
r1 = open(R1, 'r')
r3 = open(R3, 'r')

# Template to find the merging site of R1 and R3
asyn = 'ATGGATGTATTCATGAAAGGACTTTCAAAGGCCAAGGAGGGAGTTGTGGCTGCTGCTGAGAAAACCAAAC\
AGGGTGTGGCAGAAGCAGCAGGAAAGACAAAAGAGGGTGTTCTCTATGTAGGCTCCAAAACCAAGGAGGG\
AGTGGTGCATGGTGTGGCAACAGTGGCTGAGAAGACCAAAGAGCAAGTGACAAATGTTGGAGGAGCAGTG\
GTGACGGGTGTGACAGCAGTAGCCCAGAAGACAGTGGAGGGAGCAGGGAGCATTGCAGCAGCCACTGGCT\
TTGTCAAAAAGGACCAGTTGGGCAAGAATGAAGAAGGAGCCCCACAGGAAGGAATTCTGGAAGATATGCC\
TGTGGATCCTGACAATGAGGCTTATGAAATGCCTTCTGAGGAAGGGTATCAAGACTACGAACCTGAAGCC'

# Initialize the list form of the asyn sequence, hopefully initializing once
# in case of multiple comparisons to minimize computation
asynlist = [nuc for nuc in asyn]

# ascii value to probability incorrect dictionary
ascii_to_prob = pkl.load(open('ascii_to_prob.pkl', 'rb'))

# Hamming distance calculator
def Hamming(s1, s2=asyn, offset=0):
    """From two sequences return the number of mismatched values"""

    # List of letters in the first input word
    seq1list = [letter for letter in s1]
    # If the input is not asyn, create new list to compare from
    if s1 != 'aysn':
        asynlist = [letter for letter in s2]
    # Initialize the mismatch count
    count = 0
    # Go through the letters in asynlist (or other input)
    for j, nuc in enumerate(asynlist):
        # Compare the corresponding positions
        if nuc != seq1list[j]:
            # If there is a mismatch, add one to the mismatch count
            count += 1

    return count

def rev_seq(nuc, nuc_type='dna'):
    """Return the complement of each nucleotide"""

    if nuc == 'A':
        if nuc_type == 'rna':
            return 'U'
        elif nuc_type == 'dna':
            return 'T'
        else:
            return 'T'
    elif nuc == 'T':
        return 'A'
    elif nuc == 'C':
        return 'G'
    elif nuc == 'U':
        return 'A'
    else:
        return 'C'

def rev_comp(seq, seq_type = 'dna'):
    """Return the reverse complement of the input sequence"""

    # Define the length of the sequence
    seq_len = len(seq)
    # Initialize output sequence
    new_seq = ''
    # Go through each nucleotide backwards
    for letter in seq[::-1]:
        # Add new nucleotide to the end of the word
        new_seq += rev_seq(letter, seq_type)

    return new_seq


# Find the corresponding to the minimum hamming distance 
def seq_loc(s1, s2=asyn, search_range=[0,50]):
    """From two input sequences find the location via sliding window"""
   
    # Initialize the search location
    loc = 0
    # Define the window length
    s1_len = len(s1)
    # Define the length of a new input length
    if s2 != 'asyn':
        s2_len = len(s2)
    # Or define the length of the asyn sequence
    else:
        s2_len = 420
    """
    # Find the number of positions to check over
    iter_num = abs(s2_len - s1_len + 1)
    # Create list of number of mismatches per position
    counts = np.zeros(iter_num)
    # Initialize individual counts
    k = 0
    # Go through the positions in the mismatch matrix
    while k != iter_num:
        # Define the space that the two sequences will be compared over
        seq2 = s2[k:(k+len(s1))]
        # Define the number of mismatches
        mismatch = Hamming(s1,seq2,k)
        # Add the mismatch to the correct position
        counts[k] = mismatch
        # Iterate
        k += 1
    """
    counts = []
    for k in range(search_range[0], search_range[1]):
        if k+s1_len >420:
            seq1 = s1[0:(420-k)]
            seq2 = s2[k:420]
            mismatch = Hamming(seq1, seq2) / len(seq1)
        else:
            seq1 = s1
            seq2 = s2[k:(k+len(s1))]
            mismatch = Hamming(seq1, seq2) / len(seq2)
        counts.append(mismatch)

    # Find the position with the minimum number of mismatches
    min_mismatch = min(counts)

    # Go through the complete list of counts and find the location of the 
    # minimum number of mismatches
    for m, l in enumerate(counts):
        # If the value 
        if l == min_mismatch:
            loc = m + search_range[0]
    return loc 

# Initialize the document to write to
composite = open('Composite4.fastq', 'w')

# Initalize the line position
i = 2000000
# Go through the lines of the toy data
#while i < 78288632:
while i < 5000000:
    # Write the sequence name to r#_name

    if i % 4 == 0:
        print(i)
        r1_name = r1.readline().rstrip()
        r2_name = r2.readline().rstrip()
        r3_name = r3.readline().rstrip()
        composite.write(r1_name[:45])
        composite.write('\n')
    # Write the actual sequence to seq#
    elif i % 4 == 1:
        seq1 = r1.readline().rstrip()
        seq2 = r2.readline().rstrip()
        seq3 = r3.readline().rstrip()
    # Do nothing except readline, not worth saving line
    elif i % 4 == 2:
        r1.readline().rstrip()
        r2.readline().rstrip()
        r3.readline().rstrip()
    # Write the phred score to a string
    elif i % 4 == 3:
        r1_phred = r1.readline().rstrip()
        r2_phred = r2.readline().rstrip()
        r3_phred = r3.readline().rstrip()
        # Do not do anything outside of the the fourth elif, values will be
        # mismatched otherwise
        """
        # Attempt to naively find the overlap
        # Boolean attempt, assign maximum number of possible overlap mismatch 
        difference = 0.5
        # Go through the possible overlap and display if meets threshold
        for j in range(50):
            # Compare the overlap for integer number of mismatches
                print(seq1[-j:])
                print(seq3[:j])
                """
        # Search for the location of the first position for R1
        match1 = seq_loc(seq1,search_range=[0,20])
        match3 = seq_loc(seq3,search_range=[200,350])
        print(match1, match3)
        line1 = [' '] * 420
        line4 = [' '] * 420
        
        # If there is a gap
        if match1 + 300 < match3:
            initial = match3
            spacing = ' ' * (match3 - 300 - match1)
            seq_3_2 = spacing + seq3[:(420 - match1 - 300 - len(spacing))]
            phred_3_2 = spacing + r3_phred[:(420 - match1 - 300 - len(spacing))]
        # If there is an overlap
        else:
            initial = (match1 + 300) - match3
            seq_3_2 = seq3[initial:(420 + initial - match1 - len(seq1))]
            phred_3_2 = r3_phred[initial:(420 + initial - match1 - len(seq1))]
            overlap = seq3[:(match1 + 300 -match3)]
            phred_overlap = r3_phred[:(match1 + 300 - match3)]
            spacing = ' ' * match3
            line2 = spacing + overlap
            line5 = spacing + phred_overlap
            trailing = ' ' * (420 - len(line2))
            line2 += trailing
            line5 += trailing


        line1[match1:(match1 + 300)] = seq1
        line1[(match1 + 300):] = seq_3_2
        line4[match1:(match1 + 300)] = r1_phred
        line4[(match1 + 300):] = phred_3_2

        line1 = line1[:420]
        line1 = ''.join(str(x) for x in line1)
        line4 = line4[:420]
        line4 = ''.join(str(x) for x in line4)

        if (match3 + 200) < 420:
            trailing = ' ' * (420 - (match3 + 200))
            line1 += trailing
            line4 += trailing
            
        line1 += seq2
        line3 = '+'
        line4 += r2_phred
        composite.write(line1)
        composite.write('\n')
        composite.write(line2)
        composite.write('\n')
        composite.write(line3)
        composite.write('\n')
        composite.write(line4)
        composite.write('\n')
        composite.write(line5)
        composite.write('\n')

        

        # For the test data all of the positions except one(1) are 0
    # Iterate
    i += 1

# Close the files
r1.close()
r2.close()
r3.close()
composite.close()
