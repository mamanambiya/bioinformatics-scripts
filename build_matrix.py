#!/usr/bin/env python
"""
	Build matrix - creates a 2d matrix of a given
	number of rows and columns in length and outputs
	to a file. Useful for working with DupliPHY.
"""

# module imports
import sys, os, re, time

# set start time
start_time = time.time()

# get arguments
args = sys.argv[1:]

# check args
if len(args) < 2:
	print "Requires matrix row length and column length arguments (+1 as zero-base indexing)"
	sys.exit()

# define variables
col_length = int(args[0])
row_length = int(args[1])
matrix = []

# create range for first row
row_values = range(row_length)
matrix.append(list(row_values))

# do the groovy stuff
count = 0
print "Creating matrix..."
while count < row_length - 1:
	# adjust row values
	first = count + 1
	for i in range(row_length - 1, 0, -1):
		new_values = row_values
		new_values[i] = row_values[i - 1]
	new_values[0] = first
	matrix.append(list(new_values))
	# increment 
	count += 1

# save matrix to a file
matrixfile = open("matrix.txt", "w")
for row in matrix:
	matrixfile.write(' '.join([str(r) for r in row]) + "\n")
matrixfile.close()
print "Outputted to matrix.txt"
