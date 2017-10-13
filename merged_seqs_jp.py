import cPickle as pic #cPickle implements pickle in C, so it's faster
import math
from itertools import islice
import sys
filename = sys.argv[-1]

##Writiing the pickled items to .txt files to see their contents
#with open("ascii_to_prob.txt", "w") as f:
#    data = pic.load(open("ascii_to_prob_py2.pkl","rb"))
#    f.write(str(data))

##Opening pickled files for use of their dictionaries later
phred = pic.load(open("ascii_to_prob_py2.pkl","rb"))

##Determines the average Phred quality (Q) score of the given barcode.
##Returns True if Q >= 20, which is our probability cutoff.
def Q_filter(qscores):
    total = 0
    num = len(qscores)

    for i in range(len(qscores)-1):
        total += float(phred[str(qscores[i])]) #only one key to each phred[]

    avg_Phred_probability = total/num
    avg_Phred_Q = -10 * math.log(avg_Phred_probability)

    if avg_Phred_Q >= 20:
        return True
    else:
        return False

##Takes the line that only has the overlapping part in R3. Returns the start and
##stop indices of the overlap.
def get_overlap(seq):
    start = 0
    stop = 0

    for i in range(len(seq)):
        if seq[i] != " ":
            start = i
            stop = len(seq.rstrip()) ##.rstrip() so you're not counting the \n at the end
            break
    return start, stop+1 ##added the +1 so that [start:stop] would actually capture the 'stop'

##Takes R1, R3, and the phred scores for their individual nucleotides (phR1 and phR3).
##Compares the phred scores of each nucleotide in the overlap. Selects the nucleotide
##that has the lower phred score (less uncertainty) as the nucleotide in the "correct"
##a-syn overlap seq, the "good overlap". Returns the good overlap and its phred score.
##In the case that phred scores are equal but the bases differ, returns a null set.
def compare_overlaps(R1, R3, phR1, phR3):
    good_overlap_aa = ""
    good_overlap_phred = ""
    #print R1, R3
    #print phR1, phR3
    for i in range(len(R1)-1): #all same length anyway
        #print float(phred[phR1[i]]), float(phred[phR3[i]])
        #print i
        if float(phred[phR1[i]]) < float(phred[phR3[i]]):
            good_overlap_aa += R1[i]
            good_overlap_phred += phR1[i]
        elif float(phred[phR1[i]]) > float(phred[phR3[i]]):
            good_overlap_aa += R3[i]
            good_overlap_phred += phR3[i]
        elif float(phred[phR1[i]]) == float(phred[phR3[i]]) and R1[i] != R3[i]:
            return 0, 0 ##the null set
        elif float(phred[phR1[i]]) == float(phred[phR1[i]]) and R1[i] == R3[i]:
            good_overlap_aa += R1[i]
            good_overlap_phred += phR1[i]

    return good_overlap_aa, good_overlap_phred

##Replaces the nucleotides in the overlap of R1 with the nucleotides of the "correct", good overlap seq.
def paste_seqs((start, stop), R1, good_overlap):
    good_seq = R1[0:start] + good_overlap + R1[stop:]
    return good_seq

##Opens file. Merges a-syn sequence, taking the base in the overlap with the lower uncertainty.
##Returns a fastq file with the header, merged a-syn, and its individual bases' phred scores.
#with open("Composite.fastq", "r") as f:
with open(filename, "r") as f:
    with open("merged_seqs.txt", "w") as w:
        lines = f.readlines()

        for i in range(1, len(lines), 6): #just the barcodes, which are at the end of line 1 and every line 6 lines away
            if Q_filter(lines[i+3][-19:-1]) == True: #the individual amino acid's phred scores
                #print lines[i+3].rstrip()
                #print lines[i+3][-19:-1]
                (start, stop) = get_overlap(lines[i+1])
                #print "start", start, "stop", stop
                (good_overlap_aa, good_overlap_phred) = compare_overlaps(lines[i][start:stop], lines[i+1][start:stop], lines[i+3][start:stop], lines[i+4][start:stop])
                #print "here", good_overlap_aa, good_overlap_phred
                if good_overlap_aa != 0:
                    w.write(str.rstrip(lines[i-1])+ "\n") ##header
                    good_seq = paste_seqs((start, stop), str.rstrip(lines[i]), good_overlap_aa)
                    w.write(good_seq + "\n") ##merged asyn
                    w.write("+" + "\n")
                    good_phred = paste_seqs((start, stop), str.rstrip(lines[i+3]), good_overlap_phred)
                    w.write(good_phred + "\n") ##merged phred scores
