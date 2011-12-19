#!/usr/bin/python
# Filename : create_redundancy.py
# Create redundancy script
# Coded by Steve Moss - gawbul@gmail.com

# Define modules to import
import sys # could use from sys import argv here

# Check number of command-line arguments are correct
if len(sys.argv) != 4:
	# Incorrect usage
	print 'Usage: ./create_redundancy.py <infile> <redundancy> <outfile>\n'
else:
	# Load infile and output to outfile redundancy number of times
	infile = open(sys.argv[1], 'r')
	buffer = infile.read()
	infile.close()
	
	# Begin redundancy loop
	for i in range(1, int(sys.argv[2]) + 1):
		outfile = open(sys.argv[3], 'a')
		outfile.write(buffer)
	
	# Finish up, close files
	outfile.close()
	print 'Done'
