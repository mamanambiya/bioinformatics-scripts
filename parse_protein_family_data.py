#!/usr/bin/env python
""" Script to get gene members from all protein families
	corresponding to the 11 primate species in EnsEMBL
"""
# make life easier
import sys, os, time, re
import itertools
import matplotlib

# set start time
start_time = time.time()

# implementation of perl's autovivification feature
class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

# get input from command line
args = sys.argv
family_info = {}
family_members = AutoVivification()
family_freqs = []
indiv_family_freqs = {}
taxa_map = {}
genes = {}

# check we have an input file
if len(args) < 2:
	print "Need input file argument"
	sys.exit()

# set the filename
filename = args[1]
if not os.path.exists(filename):
	print "File does not exist"
	sys.exit()
	
# process the file
done = 0
infile = open(filename, "r")
print "Processing input file..."
for line in infile.readlines():
	# remove trailing whitespace
	line = line.strip()
	
	# check it is tab delimited
	if re.match("\t", line):
		print "Error: Expected a tab delimited file"
		infile.close()
		sys.exit()
	
	# split line into parts
	parts = line.split("\t")

	# should split into 6 parts
	if len(parts) != 6:
		print "Error: Expected 6 fields per line"
		infile.close()
		sys.exit()
		
	# separate parts into separate variables
	(family_id, family_desc, family_score, taxa_id, taxa_name, gene_id) = parts

	# write to hashes
	family_info[family_id] = [family_desc, family_score]
	family_members[family_id][taxa_name][gene_id] = 1
	taxa_map[taxa_id] = taxa_name
	genes[gene_id] = 1
	done += 1
infile.close()

# subset of 10 to make sure getting right data
#print dict(itertools.islice(family_info.iteritems(), 0, 10))
#print dict(itertools.islice(family_members.iteritems(), 0, 10))
#print dict(itertools.islice(taxa_map.iteritems(), 0, 10))
#print dict(itertools.islice(genes.iteritems(), 0, 10))

# let user know details of the file
print "Processed %i lines" % done
print

# set species and sort ascending
species = taxa_map.values()
species.sort()

# output in different formats
print "Outputting data files..."

# CAFE
cafefile = open("primates_cafe_input.txt", "w")
cafe_header = re.sub(" ", "", "DESCRIPTION\tID\t" + "\t".join(species))
cafefile.write(cafe_header + "\n")
# BEGFE
begfefile = open("primates_begfe_input.txt", "w")
begfe_header = re.sub(" ", "", "ID\tNUMBER\t" + "\t".join(species))
begfefile.write(begfe_header + "\n")
# DupliPHY
dupliphyfile = open("primates_dupliphy_input.txt", "w")
dupliphy_header = re.sub(" ", "", "ID\t" + "\t".join(species))
dupliphyfile.write(dupliphy_header + "\n")
dupliphymapfile = open("primates_dupliphy_map.txt", "w")
dupliphymap_header = "ID\tFAMILYID\tFAMILYDESC"
dupliphymapfile.write(dupliphymap_header + "\n")

# traverse family ids
count = 1
for fid in family_members.keys():
	family_data = []
	for sp in species:
		family_data.append(str(len(family_members[fid][sp])))
		# write pooled and individual taxa family frequencies
		family_freqs.append(len(family_members[fid][sp].keys()))
		if sp in indiv_family_freqs.keys():
			indiv_family_freqs[sp].append(len(family_members[fid][sp]))
		else:
			indiv_family_freqs[sp] = []
	# cafe
	cafe_line = family_info[fid][0] + "\t" + fid + "\t" + "\t".join(family_data)
	cafefile.write(cafe_line + "\n")
	# begfe
	begfe_line = fid + "\tnumber" + str(count) + "\t" + "\t".join(family_data)
	begfefile.write(begfe_line + "\n")
	# dupliphy
	dupliphy_line = str(count) + "\t" + "\t".join(family_data)
	dupliphyfile.write(dupliphy_line + "\n")
	dupliphymapfile.write(str(count) + "\t" + fid + "\t" + family_info[fid][0] + "\n")
	count += 1

# close file handles
dupliphymapfile.close()
dupliphyfile.close()
print "Outputted DupliPHY data file to primates_dupliphy_input.txt"
begfefile.close()
print "Outputted BEGFE data file to primates_begfe_input.txt"
cafefile.close()
print "Outputted CAFE data file to primates_cafe_input.txt"
print

# output frequencies
print "Outputting frequencies..."

# setup files
indivfreqsfile = open("primates_protein_family_freqs.txt", "w")
pooledfreqsfile = open("primates_protein_family_all_freqs.txt", "w")
pooledfreqsfile.write("family.size\tfamily.freqs\n")
indivfreqsfile.write(re.sub(" ", ".", "indivfamily.size\t" + "\t".join(species) + "\n").lower())

# get pooled frequencies
counts = dict((v, 0) for v in set(family_freqs))
for element in family_freqs:
	counts[element] += 1
for (key, value) in counts.iteritems():
	pooledfreqsfile.write(str(key) + "\t" + str(value) + "\n")

# get individual frequencies
freqs = dict((v, []) for v in set(species))
counts = AutoVivification()
for sp in species:
	for item in indiv_family_freqs[sp]:
		freqs[sp].append(item)
	counts[sp] = dict((v, 0) for v in set(freqs[sp]))
	for element in freqs[sp]:
		counts[sp][element] += 1

i = 0
while (i <= max(family_freqs)):
	found = 0
	for sp in species:
		# check if we have any keys that exist in one species but don't in others and set to size 0
		if not i in counts[sp].keys():
			counts[sp][i] = 0
		else:
			found = 1
	if found == 1:
		line = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (i, counts[species[0]][i], counts[species[1]][i], counts[species[2]][i], counts[species[3]][i], counts[species[4]][i], counts[species[5]][i], counts[species[6]][i], counts[species[7]][i], counts[species[8]][i], counts[species[9]][i], counts[species[10]][i])
		indivfreqsfile.write(line + "\n")
	i += 1
	
# close file handles
pooledfreqsfile.close()
print "Outputted pooled frequencies to primates_protein_family_freqs.txt"
indivfreqsfile.close()
print "Outputted pooled frequencies to primates_protein_family_all_freqs.txt"
print

# output some info
print "Parsed %i species" % len(taxa_map)
print "Parsed %i genes" % len(genes)
print "Parsed %i gene families" % len(family_members)
print "Parsed families from %i to %i in size" % (min(family_freqs), max(family_freqs))
print

# get end time and let user know how long we took
end_time = time.time()
total_time = end_time - start_time
print "Finished in %s seconds" % total_time

"""
# produce some graphs :D
# setup graph to plot frequencies
# my $R = Statistics::R->new();
#   
# # Run simple R commands
# my $output_file = "primates_protein_family_freqs.pdf";
# 
# $R->run('ppf_freqs <- read.delim(primates_protein_family_freqs.txt, header=T, sep = "\t")');
# 
# $R->run("pdf(file=\"$output_file\", width=7, height=7)");
# $R->run('ppf_vals <- lapply(list(x,y), function(x,y) x*y)');
# 
# #$R->run('ppf_hist <- hist(ppf_vals, PLOT=F)');
# $R->run('plot(ppf_vals, type="l", col="red", xlab="Family Size", ylab="Frequency of Family Size", main="Frequency of gene family size in 11 primate genomes")');
# $R->run('legend("topright", c("Gene Family Size"), inset=0.05, lty=1, col=c("red"))');
# $R->run('dev.off()');
# 
# # Pass and retrieve data (scalars or arrays)
# my $input_value = 1;
# #$R->set('x', $input_value);
# #$R->run(q`y <- x^2`);
# #my $output_value = $R->get('y');
# #print "y = $output_value\n";
# 
# $R->stop();
  
# show user what we have done
print "Processed " . scalar keys(%family_info) . " protein families\n";
print "Processed " . $count . " gene members\n";
print "Processed " . scalar keys(%genes) . " genes\n";
print "Processed " . scalar keys(%taxa_map) . " species\n";

# set end time
my $end_time = gettimeofday;

# calculate time taken
my $total_time = $end_time - $start_time;
print "Finished in " . $total_time . "\n";
"""
