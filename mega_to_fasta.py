#!/usr/bin/env python
"""	A file to convert all mega files in a directory
	to fasta and write them to a single output file
	all.fasta
"""

# import modules
import sys, os, glob, re

# define variables
fastaseq = []

# get input arguments
if len(sys.argv) <= 1:
	print "No path argument given"
	sys.exit()
else:
	dir = sys.argv[1]

# get all files in current directory
print "Getting all MEGA files from %s..." % dir

# traverse files list
for file in glob.glob(os.path.join(dir, '*.meg')):
	# define in path and open input file
	inpath = os.path.join(dir, file)
	inputfile = open(inpath, "r")
	# split filename by . and create output filename
	fileparts = file.split("/")
	fileparts = fileparts[-1].split(".")[0].strip()
	fileparts = re.sub("\s", "_", fileparts)
	outpath = os.path.join(dir, "all.fasta")

	# read first 4 lines which are headers
	count = 0
	while count <= 4:
		headers = inputfile.readline()
		count += 1
	# read rest of the lines	
	lines = inputfile.readlines()
	# traverse through and build sequence
	fastalines = ""
	for line in lines:
		fastalines += line.rstrip()
	fastaseq.append(">" + fileparts + "\n" + fastalines + "\n")
	inputfile.close()
#setup output file
outputfile = open(outpath, "w")
for fastaline in fastaseq:
	outputfile.write(fastaline)
outputfile.close()

print "Finished!"
