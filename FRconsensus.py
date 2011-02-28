#!/Library/Frameworks/Python.framework/Versions/2.6/bin/python
'''
-----------------------------------------------------------------------------
 By Steve Moss April 2010, some code from
 http://www.biology.duke.edu/noorlab/forward_reverse_consensus_alignment.pl
 and Dr Dave Lunt
-----------------------------------------------------------------------------
 A script to take a fasta multiple sequence alignment containing pairs of sequences from the
 same individual (e.g. individ1_For, individ1_Rev) and combine them into a single consensus
 sequence (individ1). Sequence from both Forward and Reverse are written in upper case and 
 regions contained in only one read are in lowercase.
-----------------------------------------------------------------------------
Example of correct behaviour

 data.fas (infile)
 	>SEQ1_F
 	ACGTACGTACGT--
 	>SEQ1_R
 	--GTACGTACGTAC
 data_consensus.fas (output)
 	>SEQ1
 	acGTACGTACGTac
-----------------------------------------------------------------------------
'''

# import required modules
import os, string, sys # standard imports
import re # regex requirements
import time # timing import
import datetime # date and time for log files

# write log routine
def write_log(file, message):
	logfile = open(file, "a")
	logfile.write(file + " - " + datetime.datetime.now().strftime("%A %d/%m/%Y %H:%M:%S") + "\n")
	logfile.write(message + "\n")
	logfile.close()
	return
	
# start timer
start = time.time()

# declare variables
names = []
seqbuild = []
sequences = []
forward_names = []
forward_sequences = []
reverse_names = []
reverse_sequences = []
unique_for = []
unique_rev = []
forward = []
reverse = []
consensus_names = []
consensus_sequences = []
done = 0

# display program banner
print "----------------------------------------------------------------------\n"
print "                          FRconsensus.py\n"
print "  create a consensus sequence from Forward and Reverse sequences\n"
print "                       in a fasta alignment file\n"
print "----------------------------------------------------------------------\n"

# exit if filename input argument not given
# quick and dirty - will implement getopts later
if len(sys.argv) < 2:
	print "Usage: FRconsensus.py inputfile"
	sys.exit()
else:
	inputfile = sys.argv[1]
	
# check inputfile exists
if not(os.path.isfile(inputfile)):
	print "Input file not found"
	sys.exit()

# check for .fas or .fasta extension
regex = re.match(".*?\.fas$", inputfile)
regex2 = re.match(".*?\.fasta$", inputfile)
if regex:
	outputfile = inputfile[:-4] + "_consensus.fas" # remove last four characters and append our output extension
	logfile = inputfile[:-4] + ".log" # remove last four characters and append our output extension
	errfile = inputfile[:-4] + "_error.log" # remove last four characters and append our output extension
elif regex2:
	outputfile = inputfile[:-6] + "_consensus.fas" # remove last six characters and append our output extension
	logfile = inputfile[:-6] + ".log" # remove last six characters and append our output extension
	errfile = inputfile[:-4] + "_error.log" # remove last four characters and append our output extension
else:
	print "File must be fasta format and needs \".fas\" or \".fasta\" extension.\nRecheck file and try again.\n"
	sys.exit()

# get user input
print "Supply sequence title text delimiting forward and reverse\n"
print "e.g. _For _Rev (NB this is case sensitive)\n"
# ask for text delimiting forward files e.g. "_For"
forward_delimeter = raw_input("Please indicate labeling for forward sequences: ")
# ask for text delimiting reverse files e.g. "_Rev"
reverse_delimeter = raw_input("Please indicate labeling for reverse sequences: ")

# load sequences into array
print "Loading sequences..."
acc_match = re.compile('^>.*?$') # regex for accession line
for_match = re.compile('^>.*?' + forward_delimeter + '$') # regex for forward delimeter
rev_match = re.compile('^>.*?' + reverse_delimeter + '$') # regex for reverse delimeter
# run through file
infile = open(inputfile, "r")
while not done:
	line = infile.readline()
	if not line:
		break	
	else:
		acc_regex = acc_match.match(line) # match accession line using regex
		if acc_regex:
			names.append(line) # append accession id
			if len(seqbuild) > 0:
				sequences.append("".join(seqbuild)) # if seqbuild has data then append to sequences array
				seqbuild = []
		else:
			seqbuild.append(line.rstrip("\n")) # build sequence string
sequences.append("".join(seqbuild)) # append final sequence string for last accession id as above wont catch it
seqbuild = []	
infile.close()
print "Loaded %i sequences" % len(sequences)

# check we've loaded some accession ids and not just dumped a file into a single length list
if len(names) == 0 and len(sequences) >= 0:
	print "Sequence file appears to be malformed. Please ensure it is in fasta format."
	sys.exit()
	
# create padded sequence for next padding stage using sequence length
if len(sequences) >= 1:
	padseq = "-" * len(sequences[0])

# load sequences into different forward and reverse arrays
# pad out to make equal lengths
count = 0
forcount = 0
revcount = 0
forbool = 0
revbool = 0
for name in names:
	for_regex = for_match.match(name) # match forward delimeter using regex
	rev_regex = rev_match.match(name) # match reverse delimeter using regex
	if for_regex:
		if count > 0 and forbool == 1: # if not the first item and already had a forward then pad other side - catches multiple forwards
			reverse_names.append(">REVPAD")
			reverse_sequences.append(padseq)
		elif count == len(names) - 1 and len(reverse_names) < len(forward_names) + 1:
			reverse_names.append(">REVPAD")
			reverse_sequences.append(padseq)		
		forward_names.append(name[:len(name)-(len(forward_delimeter) + 1)]) # append name minus the forward delimeter
		forward_sequences.append(sequences[count]) # append sequence
		unique_for.append(name[:len(name)-(len(forward_delimeter) + 1)]) # append name minus the forward delimeter
		forbool = 1
		revbool = 0
		forcount +=1
	elif rev_regex:
		if count > 0 and revbool == 1: # if not the first item and already had a reverse then pad other side - catches multiple reverses
			forward_names.append(">FORPAD")
			forward_sequences.append(padseq)
		elif count == len(names) - 1 and len(forward_names) < len(reverse_names) + 1:
			forward_names.append(">FORPAD")
			forward_sequences.append(padseq)	
		reverse_names.append(name[:len(name)-(len(reverse_delimeter) + 1)]) # append name minus the reverse delimeter
		reverse_sequences.append(sequences[count]) # append sequence
		unique_rev.append(name[:len(name)-(len(reverse_delimeter) + 1)]) # append name minus the reverse delimeter
		forbool = 0
		revbool = 1
		revcount += 1
	else:
		print "There has been an error identifying the forward or reverse delimeter for ", name
		print "Please rectify this before continuing"
		sys.exit()
	count += 1

# how many forward and reverse sequences do we have?
print "Loaded %i forward sequences" % forcount
print "Loaded %i reverse sequences" % revcount
print "---------------------------"

# check lists are equal length
if not len(forward_names) == len(reverse_names):
	print "List lengths should be padded to equal lengths"
	print "Please report to Steve Moss via gawbul@gmail.com"
	sys.exit()

# work out if list is unique
unique_for = set(unique_for)
unique_rev = set(unique_rev)
print "There are %i unique forward sequences" % len(unique_for)
print "There are %i unique reverse sequences" % len(unique_rev)

# work out how many matches we have
formatches = 0
revmatches = 0
for forward in unique_for:
	if forward in reverse_names:
		formatches += 1
for reverse in unique_rev:
	if reverse in forward_names:
		revmatches += 1
if formatches == revmatches: # these should be the same
	print "There are %i paired sequences" % formatches
else:
	print "Forward matches is", formatches
	print "Reverse matches is", revmatches
	print "Pair lengths are unequal, but shouldn't be"
	print "Please report to Steve Moss via gawbul@gmail.com"
	sys.exit()

# pad out any lone unmatching forward or reverse sequences
for count in range(len(forward_names)):
	if forward_names[count] == reverse_names[count]: # sequences match - do nothing but increment count
		continue
	elif forward_names[count] == ">FORPAD" or reverse_names[count] == ">REVPAD": # lists have been padded already
		continue
	elif forward_names[count] != reverse_names[count]: # sequences don't match so pad them both out
		reverse_names.insert(count, ">REVPAD")
		reverse_sequences.insert(count, padseq)
		forward_names.insert(count + 1, ">FORPAD")
		forward_sequences.insert(count + 1, padseq)
	else:
		print "Unknown error whilst checking pairs"
		print "Please report to Steve Moss via gawbul@gmail.com"

# let user known how many single forward and reverse sequences there are
print "There are %i single forward sequences" % reverse_names.count('>REVPAD')
print "There are %i single reverse sequences" % forward_names.count('>FORPAD')
# work out how many consensus sequences should be built
print "Output should be " + str(reverse_names.count('>REVPAD') + forward_names.count('>FORPAD') + formatches) + " consensus sequences"
print "------------------------------------"

# check lists are equal length
if not len(forward_names) == len(reverse_names):
	print "List lengths should be padded to equal lengths"
	print "Please report to Steve Moss via gawbul@gmail.com"
	sys.exit()

# check that we haven't messed up the matching pairs
count = 0
for forward in forward_names:
	if forward != reverse_names[count]: # do current pairs match?
		if reverse_names.count(forward) == 1 and forward_names.count(forward) == 1: # does item only appear once in both lists?
			print "Found " + forward + " in the reverse names list, but it doesn't currently match its reverse counterpart"
			print "Please report to Steve Moss via gawbul@gmail.com"
	count += 1

# go through file and append any duplicates, to make them unique
# *** TODO ***


# log the pairs to a log file using input file suffix
logout = open(logfile, "w")
logout.write(inputfile + " log - " + datetime.datetime.now().strftime("%A %d/%m/%Y %H:%M:%S") + "\n")
for count in range(len(forward_names)):
	logout.write(forward_names[count] + "\t\t\t" + reverse_names[count] + "\n")
logout.close()

# look for non matching items and add them to consensus array
# or perform consensus build if sequence names match
for count in range(len(forward_names)):
	if forward_names[count] == reverse_names[count]:
		consensus_names.append(forward_names[count]) # set name for consenus to forward name as both same
		forward = list(forward_sequences[count]) # split into individual character
		reverse = list(reverse_sequences[count]) # split into individual character
		# loop through each nt and build consensus
		for num in range(len(forward)): # go through each character in turn
			if forward[num] == reverse[num]:
				seqbuild.append(forward[num])
			elif forward[num] == " " or forward[num] == None:
				seqbuild.append(reverse[num].lower())
			elif reverse[num] == " " or reverse[num] == None:
				seqbuild.append(forward[num].lower())
			elif forward[num] == "-":
				seqbuild.append(reverse[num].lower())
			elif reverse[num] == "-":
				seqbuild.append(forward[num].lower())
			elif forward[num] == "N":
				seqbuild.append(reverse[num].lower())
			elif reverse[num] == "N":
				seqbuild.append(forward[num].lower())
			elif forward[num] == "C" and reverse[num] == "A" or forward[num] == "A" and reverse[num] == "C":
				seqbuild.append('M')
			elif forward[num] == "G" and reverse[num] == "A" or forward[num] == "A" and reverse[num] == "G":
				seqbuild.append('R')
			elif forward[num] == "T" and reverse[num] == "A" or forward[num] == "A" and reverse[num] == "T":
				seqbuild.append('W')
			elif forward[num] == "C" and reverse[num] == "G" or forward[num] == "G" and reverse[num] == "C":
				seqbuild.append('S')
			elif forward[num] == "C" and reverse[num] == "T" or forward[num] == "T" and reverse[num] == "C":
				seqbuild.append('Y')
			elif forward[num] == "G" and reverse[num] == "T" or forward[num] == "T" and reverse[num] == "G":
				seqbuild.append('K')
		consensus_build = "".join(seqbuild)
		consensus_sequences.append(consensus_build)
		seqbuild = []
	elif forward_names[count] != reverse_names[count]:
		if forward_names[count] == ">FORPAD": # is it one of the padded items?
			consensus_names.append(reverse_names[count])
			consensus_sequences.append(reverse_sequences[count])
		elif reverse_names[count] == ">REVPAD": # is it one of the padded items?
			consensus_names.append(forward_names[count])
			consensus_sequences.append(forward_sequences[count])
		else: # must be a different single forward and reverse sequence
			consensus_names.append(forward_names[count])
			consensus_sequences.append(forward_sequences[count])
			consensus_names.append(reverse_names[count])
			consensus_sequences.append(reverse_sequences[count])
# let user know we're done here
print "Conversion done"

# write output
# process output
outfile = open(outputfile, "w")
for count in range(len(consensus_names)):
	outfile.write(consensus_names[count] + "\n")
	outfile.write(consensus_sequences[count] + "\n")
outfile.close()

#print out completion and output file notification
print "A total of %i consensus sequences were identified" % len(consensus_sequences)
print "Consensus sequences written to file " + outputfile
# end timer
end = time.time()
total = end - start

# let the user know we've finished
print "Finished in %s seconds\n" % str(datetime.timedelta(seconds=total))
print "-----------END-----------\n"
	