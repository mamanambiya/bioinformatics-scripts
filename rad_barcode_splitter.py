"""
A RAD/FASTQ barcode splitter
Takes a single FASTQ input file as an argument and expects a barcodes
file in the current directory with each barcode on an individual line
Coded by Steve Moss
http://twitter.com/gawbul
gawbul@gmail.com
"""

# import modules needed
from Bio import SeqIO
import sys, re, os, time

# set starttime
starttime = time.time()

# get input from command line
args = sys.argv[1:] # miss out argument 0 as that is the script filename

# check we have at least one input argument
if (args != 1):
	print "Need a filename as input."
	sys.exit()

# set filename from input arguments
inputfile = args[0]

# check extension is fastq
if (not re.match("^.*?\.fastq$", inputfile)):
	print "Expecting a FASTQ file extension."
	sys.exit()

# check barcodes file exists
if (not os.path.exists("barcodes")):
	print "Could not find the \"barcodes\" input file in the cwd."
	sys.exit()

# read in the barcodes
barcodes = open("barcodes", "rU").readlines()

# let user know the score
print "Processing fastq file for %d barcode(s)..." % len(barcodes)

# iterate over barcodes
for barcode in barcodes:
	# remove newline
	barcode = barcode.rstrip("\n")
	# check barcode is ACGT
	if (not re.match("^[ACGT]+$", barcode)):
		print "Expecting a DNA alphabet."
		sys.exit()

	# iterate over inputfile and read in barcode specific sequences
	barcode_re = re.compile("^" + barcode)
	seq_iterator = SeqIO.parse(open(inputfile, "rU"), "fastq")
	barcode_sequences = [record for record in seq_iterator if (barcode_re.match(str(record.seq)))] # need to convert record.seq to string here

	# set outputfile name
	outputfile = inputfile[:-6] + "_" + barcode + ".fastq" # remove the .fastq from input file and append with barcode

	# write to output
	SeqIO.write(barcode_sequences, open(outputfile, "a"), "fastq")
	
	# let user know what we've done
	print "Outputted %d sequence(s) matching %s barcode to %s." % (len(barcode_sequences), barcode, outputfile)

# set end time
endtime = time.time()

#calculate time
totaltime = endtime - starttime

# let user know we're done
print "Finsihed in %s seconds" % totaltime