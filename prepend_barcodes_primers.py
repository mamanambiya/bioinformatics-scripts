#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python

# module imports
from Bio import SeqIO
import sys, os, re

# get input arguments
args = sys.argv
if len(args) < 2:
	print "ERROR: You need three input arguments for the fasta and qual file you wish to process"
	sys.exit(0)

# variables
fastafile = args[1]
outfasfile = fastafile + ".pre"
qualfile = args[2]
outqualfile = qualfile + ".pre"

barcodes_map = {"MID1":"ACGAGTGCGT",
				"MID2":"ACGCTCGACA",
				"MID3":"AGACGCACTC",
				"MID4":"AGCACTGTAG",
				"MID6":"ATATCGCGAG",
				"MID7":"CGTGTCTCTA",
				"MID8":"CTCGCGTGTC",
				"MID9":"TAGTATCAGC",
				"MID11":"TGATACGTCT",
				"MID12":"TACTGAGCTA",}

# open fasta file and process
print "Processing fasta file %s..." % fastafile
fastafh = open(fastafile, "rU")
fasoutfh = open(outfasfile, "w")
count = 0
for record in SeqIO.parse(fastafh, "fasta"):
	header = record.id
	header_parts = header.split('_')
	sequence = barcodes_map[header_parts[0]] + record.seq
	record.seq = sequence
	SeqIO.write(record, fasoutfh, "fasta")
	count += 1
fasoutfh.close()
fastafh.close()
print "Processed %i fasta sequences" % count


# open qual file and process
print "Processing qual file %s..." % qualfile
qualfh = open(qualfile, "rU")
qualoutfh = open(outqualfile, "w")
count = 0
for record in SeqIO.parse(qualfh, "qual"):
	for i in range(10):
		record.letter_annotations["phred_quality"].insert(0, 30)
	SeqIO.write(record, qualoutfh, "qual")
	count += 1
qualfh.close()
qualoutfh.close()
print "Processed %i qual scores" % count
qualoutfh.close()
qualfh.close()
