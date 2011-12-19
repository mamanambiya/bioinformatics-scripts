# imports
from Bio import SeqIO
import sys

# check inputs
if len(sys.argv) < 1:
	print "Require input file as argument"
	sys.exit()
else:
	inputfile = sys.argv[1]
	outputfile = inputfile[-4] + ".phy"

# load inputfile
count = 0
infile = open(inputfile, "rU")
outfile = open(outputfile, "w")
for record in SeqIO.parse(infile, "fasta"):
	SeqIO.write(record, outfile, "phylip-relaxed")
	count += 1
outfile.close()
infile.close()

print "Processed %i sequences" % count