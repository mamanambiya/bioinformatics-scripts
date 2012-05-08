#!/usr/bin/env python
# script to change the fasta description line to 
# just have the accession id

from Bio import SeqIO
import sys, time

# set start time
start_time = time.time()

# check we have required number of input arguments
# the script filename is counted as one hence < 2
if len(sys.argv) < 2:
	print "Requires input file argument"
	sys.exit()
	
# set input and output filenames
inputfile = sys.argv[1]
outputfile = inputfile.split(".")[0] + "_fixed.fasta"

# open files for reading and writing
infile = open(inputfile, "r")
outfile = open(outputfile, "w")

# process the fasta records
count = 0
print "Processing records..."
for record in SeqIO.parse(infile, "fasta"):
	accession = record.description.split('|')[3] # we just want the accession number
	record.id = accession
	record.description = accession
	SeqIO.write(record, outfile, "fasta")
	count += 1
#close files
outfile.close
infile.close
print "Processed %i records!" % count

#display elapsed time
print "Finished in %f seconds" % (time.time() - start_time)
