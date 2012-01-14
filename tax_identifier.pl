use strict;
use warnings;
use Bio::DB::Taxonomy;
use Bio::Tree::Tree;

my @args = @ARGV;

if (scalar(@args) < 1) {
	die("Expect at least one input argument\n");
}

#my @taxonids = (515482, 515474);
my @taxonids = @args;
my @lineages = ();

my $db = Bio::DB::Taxonomy->new(-source => 'entrez');

foreach my $taxonid (@taxonids) {
	my $taxon = $db->get_taxon(-taxonid => $taxonid);
	my $tree = Bio::Tree::Tree->new(-node => $taxon);
	my @taxa = $tree->get_nodes;
	my @tids = ();
	foreach my $t (@taxa) {
		unshift(@tids, $t->id());
	}
	push(@lineages, $taxonid . "\t|\t" . $taxon->scientific_name() . "\t|\t" . "@tids");
}

foreach my $lineage (@lineages) {
	print "$lineage\n";
}
