#!/usr/bin/env python
"""
Python script to retrieve KEGG gene entry for a number of different genes
Coded by Steve Moss (gawbul [at] gmail [dot] com
http://about.me/gawbul
"""

# import required modules
from SOAPpy import WSDL

# setup kegg wsdl
kegg_wsdl = 'http://soap.genome.jp/KEGG.wsdl'
kegg_service = WSDL.Proxy(kegg_wsdl)

# setup array of gene names
gene_names = ("ALDOA", "BHLHB3", "PKM2", "P4HA1", "EPO")

# iterate of gene_names and retrieve sequences
for gene_name in gene_names:
    # use bfind first to find the list of genes for each query
	# limit to hsa (homo sapiens)
	gene_entries = kegg_service.bfind("genes " + gene_name + " hsa").rstrip("\n").split("\n") # returns str so split on \n
	print "Found %d entries for %s" % (len(gene_entries), gene_name)
	
	# iterate over gene_entries
	for gene_entry in gene_entries:
		# just use the first part of the string (e.g. hsa:226) to retrieve
		# the sequences in fasta format (-f)
		results = kegg_service.bget("-f " + gene_entry.split(" ")[0])
		# print results to screen
		print results