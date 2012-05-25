#!/usr/bin/env python

# imports
import os, sys, re, operator

# variables
taxa_cloud = {}

# check input arguments
if len(sys.argv) < 2:
	raise IOError("Need input file")

# set input file as first arg
input_file = sys.argv[1]

# check file exists
if not os.path.exists(input_file):
	raise IOError("File doesn't exist")
	sys.exit()

# traverse results files
in_file = open(input_file, "r")
while 1:
	line = in_file.readline()
	if not line:
		break
	line.strip()
	parts = line.split("|")
	for part in parts:
		if re.search("\n", part):
			part == part[:-2]
		if taxa_cloud.has_key(part):
			taxa_cloud[part] += 1
		else:
			taxa_cloud[part] = 1
in_file.close()

# sort by counts
sorted_taxa = sorted(taxa_cloud.iteritems(), key=operator.itemgetter(1), reverse=True)

# print to out file
out_file = open("taxa_cloud.txt", "w")
for item in sorted_taxa:
	out_file.write(item[0].strip() + " = " + str(item[1]) + "\n")
out_file.close()
	