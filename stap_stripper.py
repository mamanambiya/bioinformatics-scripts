#!/usr/bin/env python

# imports
import os, sys, re

# variables
files = []
results_files = []
line = ""
# check input arguments
if len(sys.argv) < 2:
	raise IOError("Need input directory")
	
base = sys.argv[1]
files = os.listdir(base)

# traverse files
count = 0
for file in files:
	if re.match("^.*?\.results$", file):
		results_files.append(file)
		count += 1
		if count == 250:
			break
			

# traverse results files
for file in results_files:
	in_path = os.path.join(base, file)
	out_path = os.path.join(os.getcwd(), "58988_stap_output_results.txt")
	in_file = open(in_path, "r")
	while 1:
		line = in_file.readline()
		if not line:
			break
		regex = re.match("^.*?\tTREE2=.*?\|(.*?)\tDOMAIN=[A-Za-z]\|INPUT$", line)
		if regex:
			out_file = open(out_path, "a")
			out_file.write(regex.group(1) + "\n")
			out_file.close()
	in_file.close()
	
print "Done!"