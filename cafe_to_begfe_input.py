#!/usr/bin/env python
""" Lets the user convert a cafe input format file to a BEGFE input format file
	Requires the CAFE file to be in the format DESCRIPTION\tID\tSpecies1\tSpecies2... etc
"""

# imports
import sys, os

#define some global variables

# get command line inputs and do checks
args = sys.argv
if len(args) < 2:
	print "We require an input file to convert!"
	sys.exit()

# assign inputfile and check exists
inputfile = args[1]
if not os.path.exists(inputfile):
	print "The filename (%s) you specified does not exist" % inputfile
	sys.exit()

# set output filename and let user know we are converting
outputfile = inputfile.split('.')[0] + ".begfe"
print "Converting file format to BEGFE input..."

# set file handles
infile = open(inputfile, "rU")
outfile = open(outputfile, "w")

# split header line and write new header
header_parts = infile.readline().strip().split("\t")
new_header = "ID\tNUMBER\t" + "\t".join(header_parts[2:])
outfile.write(new_header + "\n") # new header in format ID NUMBER SPECIES1... ETC

# traverse through inputfile
count = 1
for line in infile.readlines():
	parts = line.strip().split("\t")
	newline = parts[1] + "\t" + "number" + str(count) + "\t" + "\t".join(parts[2:])
	outfile.write(newline + "\n")
	count += 1

# close file handles
outfile.close()
infile.close()

# set lines processed and let user know we're done and where to find things
print "Saved %d lines to %s" % (count, outputfile)