#!/Library/Frameworks/Python.framework/Versions/2.6/bin/python
'''
	unique_fasta_desc_num.py
	Coded by Steve Moss July 2010
	gawbul@gmail.com
	
	Take a multifasta file and make the description line unique with the sequence number
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
if len(sys.argv) < 2:
	print "Usage: unique_fasta_desc_num.py inputfile"
	sys.exit()
else:
	inputfile = sys.argv[1]
	outputfile = inputfile[:-6] + "_uniq-desc" + ".fasta"

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
count = 1
infile = open(inputfile, "r")
while not done:
	line = infile.readline()
	if not line:
		break
	else:
		regex = re.search("^>", line)
		if regex:
			# shortern the description line if needed
			acc_ids.append(">SEQ_" + str(count))
			count += 1
		else:
			sequences.append(line.rstrip("\n"))
infile.close()
# check loaded properly
if len(sequences) == len(acc_ids):
	print "Loaded %i sequences" % len(sequences)
else:
	print "Error loading sequences - contact gawbul@gmail.com"

# write output
# process output
print "Writing output..."
outfile = open(outputfile, "w")
count = 0
for index in range(len(sequences)):
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