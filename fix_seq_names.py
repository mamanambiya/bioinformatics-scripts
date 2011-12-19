# imports
from Bio import SeqIO
import sys, os, glob

######
# this script isn't finished
#######

# variables
inputfiles = []
outputfiles = []
accession_map = {	"MID1" : "DL1_C_07_F",
					"MID2" : "DL2_C_03_F",
					"MID3" : "DL3_C_09_F",
					"MID4" : "DL4_C_03_M",		
					"MID6" : "DL5_C_14_M",		
					"MID7" : "DL6_O_13_F",		
					"MID8" : "DL7_O_16_F",		
					"MID9" : "DL8_O_17_F",		
					"MID11" : "DL9_O_01_M",		
					"MID12" : "DL10_O_04_M"}

# give input directory and filename
if len(sys.argv) < 1:
	print "Need directory containing sequences"
	sys.exit()
else:
	input_dir = sys.argv[1]
	
# check directory exists
if not os.path.exists(input_dir):
	print "You entered a non-existent directory name (%s)" % input_dir
	sys.exit()
	
# get list of subdirectories
dirs = glob.glob(input_dir)

# get list of files matching .fna
files = 

# load inputfile
for file in inputfiles:
	infile = open(file, "rU")
	outputfile = file[-4] + ".fasta"
	outfile = open(outputfile, "w")
for record in SeqIO.parse(infile, "fasta"):
	SeqIO.write(record, outfile, "fasta")
	count += 1
outfile.close()
infile.close()

print "Processed %i sequences" % count