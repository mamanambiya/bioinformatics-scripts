#!/usr/bin/env python

"""
This script will load a multiFASTA input file and stream it into STAP++
For MSc practical class using gut microbiota data
Coded by Steve Moss
27th April 2011
gawbul@gmail.com
"""

# imports
import os, sys, getopt, subprocess
from time import time
from Bio import SeqIO

# variables
stap_path = "/home/steve/Desktop/msc_practical/STAP/rRNA_pipeline_scripts/rRNA_pipeline_for_one_pp.pl"

def main():
	try:
		# get options
		opts, args = getopt.getopt(sys.argv[1:], "hvi:o:", ["help", "version", "input=", "ouput="])
	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)
	input_file = None
	output_dir = None
	# check we have input and output location
	for opt, arg in opts:
		if opt in ("-v", "--version"):
			version()
			sys.exit()
		elif opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-i", "--input"):
			input_file = arg
			check_input_exists(input_file)
		elif opt in ("-o", "--output"):
			output_dir = arg
			check_input_exists(output_dir)
		else:
		    assert False, "unhandled option"
	 # run STAP streamer
	if input_file == None or output_dir == None:
		usage()
		sys.exit()
	else:
		stream_stap(input_file, output_dir)

def version():
	print "run_STAP.py version 0.1"
	print

def usage():
	print "run_STAP.py usage:"
	print "\t-h or --help\t\tDisplay usage"
	print "\t-v or --version\t\tDisplay version information"
	print "\t-i or --input\t\tProvide input filename"
	print "\t-o or --output\t\tProvide output directory"
	print

def check_input_exists(inputfile=None):
	if not os.path.exists(inputfile):
		raise IOError("Input file not found")
	
def check_output_exists(outputdir=None):
	if not os.path.exists(outputdir):
		raise IOError("Output directory not found")

def stream_stap(inputfile, outputdir):
	# go through each fasta record in turn	
	for seq_record in SeqIO.parse(inputfile, "fasta"):
		# save to output directory
		stapinput = os.path.join(outputdir, seq_record.id + ".fasta")
		SeqIO.write(seq_record, stapinput, "fasta")
		# run STAP
		print "Running %s through STAP..." % stapinput			
		p = subprocess.Popen(["perl", stap_path, "-i", stapinput, "-o", outputdir, "-d", "P"])
		p.communicate()
	
if __name__ == "__main__":
	start_time = time()
	main()
	end_time = time()
	total_time = end_time - start_time
	print "Finished in %s seconds" % total_time
