#!/usr/bin/env perl
# A perl script to get the taxonomic lineage from NCBI Entrez

# catch any problems, keep things neat
use strict;
use warnings;

# import modules
use Bio::DB::Taxonomy;
use Bio::Tree::Tree;
use Data::Dumper;
use Time::HiRes qw(gettimeofday);

# set start time
my $start_time = gettimeofday;

# setup variables
my @binomials = ();
my $failed_seqs = 0;
my $seqs_count = 0;
my %unique_binomials = ();
my @ncbi_taxonids = ();
my @ncbi_names = ();
my @ncbi_names_wait = ();
my ($outputfile, $outputfile2) = "";
my $numids_count = 0;
my $ncbi_failed = 0;
my $nodesfile = "/Volumes/KINGSTON/Data/taxdump/nodes.dmp";
my $namesfile = '/Volumes/KINGSTON/Data/taxdump/names.dmp';

# get input arguments
my @args = @ARGV;

# check we have an input file from the user
if (scalar(@args) < 1) {
	print "ERROR: You need to provide an input file as an argument!\n";
	die();
}

# setup access to Entrez DB
print "Processing NCBI taxonomy files...\n";
my $db = Bio::DB::Taxonomy->new(-source => 'flatfile',
								-nodesfile => $nodesfile,
								-namesfile => $namesfile,);
print "Done!\n";

# assign input filename
my $inputfile = $args[0];

# load our input file and parse the binomial
open INFILE, "<$inputfile" or die $!;
print "Processing inputfile...\n";
while (my $line = <INFILE>) {
	# check if we have the fasta header line
	if ($line =~ m/^>/) {
		my @parts = split(/:/, $line); # splits on the : after 'best species guess text in Metaxa output file
		chomp(@parts);
		my $name = $parts[0];
		$name =~ s/>(MID[0-9]+_[A-Z0-9]+)\s.*/$1/;
		my $binomial = $parts[1];
		$binomial =~ s/^\s+//; # remove leading spaces
		if ($binomial eq '') {
			$failed_seqs++;
			$seqs_count++;
			next;
		}
		elsif ($binomial =~ /^[0-9]+$/) {
			push(@ncbi_taxonids, $binomial);
			push(@ncbi_names, $name);
			$numids_count++;
			next;
		}
		else {
			if (defined $unique_binomials{$binomial}) {
				$unique_binomials{$binomial}++;
			}
			else {
				$unique_binomials{$binomial} = 1;
			}
		}
		$binomial =~ s/^uncultured\s//; # remove leading uncultured
 		$binomial =~ s/\s\({1}.*\){0,1}$//; # remove common names in parentheses
 		$binomial =~ s/\ssp|cf|subsp|var|et\sal\..*$//; # remove trailing sp.
		$binomial =~ s/\s[A-Z0-9-]*$//; # remove clone IDs
		$binomial =~ s/\.+//; # remove dots
		$binomial =~ s/\s{2,}/\s/; # replace long spaces with single space
		push(@binomials, $binomial);
		push(@ncbi_names_wait, $name);
		$seqs_count++;
	}
}
close INFILE;
my $actual = $seqs_count - $failed_seqs;
print "Processed $seqs_count sequences ($actual passed)\n";
print "Failed on $failed_seqs\n";
print "Numeric IDs pushed straight to taxon ID list: $numids_count\n";

# output the counts to a file
$outputfile = "species_counts.txt";
open OUTFILE, ">$outputfile" or die $!;
for my $key (sort {$unique_binomials{$a}<=>$unique_binomials{$b}} keys %unique_binomials) {
	print OUTFILE "$key = $unique_binomials{$key}\n";
}
print OUTFILE "\nProcessed $seqs_count sequences ($actual passed)\n";
print OUTFILE "Failed on $failed_seqs\n";
print OUTFILE "Numeric IDs pushed straight to taxon ID list: $numids_count\n";
close OUTFILE;
print "Outputted binomial counts to $outputfile\n\n";

# traverse binomials and get NCBI taxon
# also output taxon names
print "Retrieving NCBI taxon IDs...\n";
my $count = 0;
$outputfile2 = "ncbi_taxon_names.txt";
open OUTFILE2, ">$outputfile2" or die $!;
for my $binomial (@binomials) {
	print OUTFILE2 "$binomial\n";
	my $taxonid = $db->get_taxonid($binomial);
	if (defined($taxonid)) {
		if ($taxonid ne 'undef') {
			push(@ncbi_taxonids, $taxonid);
			push(@ncbi_names, $ncbi_names_wait[$count]);
		}
	}
	$count++;
}
print "Retrieved $count taxon IDs\n";
print "Failed on $ncbi_failed IDs\n";
close OUTFILE2;

print scalar(@ncbi_taxonids) . "\n";
print scalar(@ncbi_names) . "\n";

# output NCBI taxon IDs to a file
print "Outputting NCBI taxon IDs to $outputfile...\n";
$outputfile = "ncbi_taxon_ids.txt";
open OUTFILE, ">$outputfile" or die $!;
my $num = 0;
while ($num < scalar(@ncbi_taxonids) + 1) {
	print OUTFILE $ncbi_names[$num] . "\t" . $ncbi_taxonids[$num] . "\n" if defined $ncbi_names[$num] && defined $ncbi_taxonids[$num];
	$num++;
}
close OUTFILE;
print "Done!\n";

# set end time
my $end_time = gettimeofday;
my $total_time = $end_time - $start_time;
print "Finished in $total_time\n";