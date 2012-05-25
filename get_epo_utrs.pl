#!/usr/bin/env perl
# Perl script to retrieve the 3'-UTR sequence for 12 eutherian mammals
# Coded by Steve Moss (gawbul@gmail.com)
# http://stevemoss.ath.cx/

# make things easier
use strict;
use warnings;

#import EnsEMBL and BioPerl modules
use Bio::EnsEMBL::Registry;
use Bio::SeqIO;
use Data::Dumper;

# setup array of all epo mammals
my @epo_mammals = ("homo_sapiens", "gorilla_gorilla", "pan_troglodytes", "pongo_abelii", "macaca_mulatta", "callithrix_jacchus", "mus_musculus", "rattus_norvegicus", "equus_caballus", "canis_familiaris", "sus_scrofa", "bos_taurus");

# connect to EnsEMBL
my $registry = 'Bio::EnsEMBL::Registry';
$registry->load_registry_from_db(	-host => 'ensembldb.ensembl.org',
									-user => 'anonymous');

# use Bio::SeqIO to write sequence to STDOUT
my $outseq = Bio::SeqIO->new(	-fh => \*STDOUT,
								-format => 'FASTA');
										
# loop over the mammals
foreach my $mammal (@epo_mammals) {
	# get gene adaptor
	my $gene_adaptor = $registry->get_adaptor($mammal, 'Core', 'Gene');
	
	# fetch all genes
	my @gene_ids = @{$gene_adaptor->list_stable_ids()};

	# traverse through genes
	foreach my $gene_id (@gene_ids) {
		# get gene
		my $gene = $gene_adaptor->fetch_by_stable_id($gene_id);
		
		# get canonical transcript
		my $transcript = $gene->canonical_transcript();
		
		# check gene has a transcript associated
		unless (defined $transcript) {
			next;
		}
		
		# get 3'-UTR - returns a Bio::Seq object
		my $tputr = $transcript->three_prime_utr();
		
		# check transcript has a 3'-UTR annotated
		unless (defined $tputr) {
			next;
		}
		
		# print to STDOUT
		print $outseq->write_seq($tputr) . "\n";
	}
}