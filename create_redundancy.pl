#!/usr/bin/perl
#------------------------------------------------------------------------#
# Perl script to create multiple redundancy in a fasta file for testing  #
# external redundancy scripts.                                           #
# Coded by Steve Moss                                                    #
# Email: gawbul@gmail.com					                             #
#------------------------------------------------------------------------#

use strict;
use warnings;

# define variables
my $filename="";
my $redundancy="";
my $output="";
my $buffer="";

# Check for valid usage; if incorrect number of arguments then display usage and exit
if($#ARGV != 2) {
	print("Usage: ./create_redundancy.pl <infile> <redundancy> <outfile>\n");
}
else {
	# Assign variables
	$filename = $ARGV[0];
	$redundancy = $ARGV[1];
	$output = $ARGV[2];
	
	# Open file and chomp to ensure things are read in properly
	# Read file to buffer
	undef $/;
	open(FAS_IN, $filename) or die "Error: Couldn't open $filename!";
	$buffer = <FAS_IN>;
	close(FAS_IN);
	
	# Create redundancy in file using number given in command-line arguments
	for (my $i = 1; $i <= $redundancy; $i++) {
		open(FAS_OUT, ">>$output");
		print FAS_OUT $buffer;
	}
	close FAS_OUT;
	print "Done\n";
}
