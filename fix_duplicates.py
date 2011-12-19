# imports
from Bio import SeqIO
import sys

# variables
records_dict = {}
formats = ["fasta", "qual"]

if len(sys.argv) < 2:
	print "Require input file as argument"
	sys.exit()
else:
	inputfile = sys.argv[1]
	format = sys.argv[2]
	if not format in formats:
		format = "fasta"
	outputfile = inputfile + "_output

# load inputfile
num_append = 1
infile = open(inputfile, "rU")
outfile = open(outputfile, "w")
for record in SeqIO.parse(infile, format):
	if records_dict.has_key(record.id):
		records_dict[record.id] += 1
		record.id += str(num_append)
		SeqIO.write(record, outfile, format)
	else:
		records_dict[record.id] = 1
		SeqIO.write(record, outfile, format)
	num_append += 1
outfile.close()
infile.close()

print "Processed %s sequences" % (num_append - 1)

# check which accession IDs have duplicates
# and how many
for key,val in records_dict.items():
	if val > 1:
		print key + " = " + str(val) + " ",
print

