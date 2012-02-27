#!/usr/bin/env python
"""
A Python script to filter out certain organisms from a QIIME generated otu_table.txt file
"""

# imports
import os, sys, re

# setup variables
filter_orgs = ["p__Fungi", "p__Stramenopiles", "p__Viridiplantae"]
header_lines = []
filter_count = 0

# get program input
args = sys.argv[1:]

# check we have a filename argument
if len(args) < 1:
	print "Expecting filename as input"
	sys.exit()

# set filenames
filename = args[0]
output_filename = filename[:-4] + "_filtered.txt"

# check the file exists
if not os.path.exists(filename):
	print "File doesn't exist"
	sys.exit()

# open the files
input_file = open(filename, "r")
output_file = open(output_filename, "w")
# read in first two lines
for i in range(2):
	header_lines.append(input_file.readline().rstrip("\n"))
# write headers to output file
for header in header_lines:
	output_file.write(header + "\n")
# iterate over lines
total_count = 0
for line in input_file.readlines():
	line = line.rstrip("\n") # remove trailing whitespace
	parts = line.split("\t")
	# check we have 12 parts
	if len(parts) != 12:
		print "Expecting 12 tab-delimited columns, not %d." % len(parts)
		sys.exit()
	# set variables
	otu_id = parts[0]
	lineage = parts[-1]
	# split lineage into parts
	lineage_parts = lineage.split(";")
	# check at least 3 parts
	if len(lineage_parts) >= 3:
		phylum = lineage_parts[2]
	else:
		continue
	# check if we match any of the filters
	if not phylum in filter_orgs:
		# write only non matches to output file
		output_file.write(line + "\n")
		filter_count += 1
	total_count += 1
output_file.close()
input_file.close()

# let user know we're done
removed_count = total_count - filter_count
print "%d lines (of %d) written to %s (%d not written)" % (filter_count, total_count, output_filename, removed_count) 