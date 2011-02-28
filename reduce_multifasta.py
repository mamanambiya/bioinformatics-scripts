#!/Library/Frameworks/Python.framework/Versions/2.6/bin/python
'''
	reduce_multifasta.py
	Coded by Steve Moss July 2010
	gawbul@gmail.com
	
	Take a multifasta file and reduce it down to only a given number of elements
'''

# import required modules
import os, string, sys # standard imports
import re # regex requirements
import time # timing import
import datetime # date and time for log files

# start timer
start = time.time()

# declare some variables
done = 0 # used in while loops
acc_ids = [] # stores the acc ids
sequences = [] # stores the sequences

# exit if filename input argument not given
# quick and dirty - will implement getopts later
if len(sys.argv) < 3:
	print "Usage: reduce_multifastsa.py inputfile number"
	sys.exit()
else:
	inputfile = sys.argv[1]
	number = int(sys.argv[2])
	outputfile = inputfile[:-6] + "_" + str(number) + ".fasta"

# check inputfile exists
if not(os.path.isfile(inputfile)):
	print "Input file not found"
	sys.exit()

# check for .fasta extension
regex = re.search("\.fasta$", inputfile)
if not regex:
	print "File must have \".fasta\" extension.\nRecheck file and try again."
	sys.exit()

# load file and enter values into an array
print "Loading sequences..."
# run through file
infile = open(inputfile, "r")
count = 0
while not done:
	line = infile.readline()
	if not line:
		break
	else:
		regex = re.search("^>", line)
		if regex:
			acc_ids.append(line.rstrip("\n"))
		else:
			sequences.append(line.rstrip("\n"))
	count += 1
	if count >= (number * 2) and len(sequences) == len(acc_ids):
		break
infile.close()
if len(sequences) == len(acc_ids):
	print "Loaded %i sequences" % len(sequences)
else:
	print "Error loading sequences - contact gawbul@gmail.com"

# write output
# process output
print "Writing output..."
outfile = open(outputfile, "w")
count = 0
for index in range(number):
	outfile.write(acc_ids[index] + "\n")
	outfile.write(sequences[index] + "\n")
	count += 1
outfile.close()
print "Outputted %i sequences" % count

# end timer
end = time.time()
total = end - start

# let the user know we've finished
print "Finished in %s seconds\n" % str(datetime.timedelta(seconds=total))