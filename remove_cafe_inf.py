#!/usr/bin/env python
""" Script to remove any particularly large branch changes from cafe input file
	and save removed files to new output
"""

# some imports
import sys, os, time, re

# variables
# adjust this for max - min cut-off
size_cut_off = 20
# number columns in input file
column_count = 13

# set start time
start_time = time.time()

# get input from command line
args = sys.argv

# check we have an input file
if len(args) < 2:
	print "Need input file argument"
	sys.exit()

# set the filename
filename = args[1]
if not os.path.exists(filename):
	print "File does not exist"
	sys.exit()
	
# process the file
done = 0
infile = open(filename, "r")
removedcafefile = open("primates_cafe_input_removed.txt", "w")
noninfcafefile = open("primates_cafe_input_noninf.txt", "w")
print "Processing input file..."
# read header line first
cafe_header = infile.readline().strip()
# write headers back
removedcafefile.write(cafe_header + "\n")
noninfcafefile.write(cafe_header + "\n")
# traverse lines in cafe input file
removedcount = 0
noninfcount = 0
for line in infile.readlines():
	# remove trailing whitespace
	line = line.strip()
	
	# check it is tab delimited
	if re.match("\t", line):
		print "Error: Expected a tab delimited file"
		sys.exit()
	
	# split line into parts
	parts = line.split("\t")

	# should split into 13 parts
	if len(parts) != column_count:
		print "Error: Expected %s fields per line" % column_count
		sys.exit()
	
	# separate parts into separate variables
	(family_desc, family_id) = parts[0:2]
	sizes = parts[2:]
	
	# check input
	family_sizes = []
	for size in sizes:
		family_sizes.append(int(size))
	if (max(family_sizes) - min(family_sizes)) > size_cut_off:
		# write this line to removed output
		removedcafefile.write(line + "\n")
		removedcount += 1
	else:
		# write this to non-inf output
		noninfcafefile.write(line + "\n")
		noninfcount += 1
	done += 1
noninfcafefile.close()
removedcafefile.close()
infile.close()

# tell user what we've done
print "Parsed %s lines with -inf values (>%s)" % (removedcount, size_cut_off)
print "Parsed %s non-inf lines" % noninfcount
# should total 49737
print "Parsed a total of %s lines" % (removedcount + noninfcount)

# get end time and let user know how long we took
end_time = time.time()
total_time = end_time - start_time
print "Finished in %s seconds" % total_time