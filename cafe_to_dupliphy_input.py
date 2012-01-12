#!/usr/bin/env python
""" Lets the user convert a cafe input format file to a DupliPHY input format file
	Requires the CAFE file to be in the format DESCRIPTION\tID\tSpecies1\tSpecies2... etc
	Creates the new input file and a mapping file to map the description and ID from the CAFE
	file to the new DupliPHY input file.
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
outputfile = inputfile.split('.')[0] + ".dupliphy"
mappingfile = outputfile + "_map"
print "Converting file format to DupliPHY..."

# set file handles
infile = open(inputfile, "rU")
outfile = open(outputfile, "w")
mapfile = open(mappingfile, "w")

# split header line and write new header
header_parts = infile.readline().strip().split("\t")
new_header = "\t".join(header_parts[1:])
outfile.write(new_header + "\n")
mapfile.write("DupliPHY ID\t" + "\t".join(header_parts[0:2]) + "\n")

# traverse through inputfile
count = 0
for line in infile.readlines():
	parts = line.strip().split("\t")
	newline = str(count) + "\t" + "\t".join(parts[2:])
	outfile.write(newline + "\n")
	mapfile.write(str(count) + "\t" + "\t".join(parts[0:2]) + "\n")
	count += 1
# close file handles
mapfile.close()
outfile.close()
infile.close()

# set lines processed and let user know we're done and where to find things
print "Saved %d lines to %s and %s" % (count, outputfile, mappingfile)