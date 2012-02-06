#!/usr/bin/env python

#imports
import sys, os, re, random

# variables
fish = ['Theragra_chalcogramma', 'Theragra_finnmarchica', 'Gadus_macrocephalus', 'Gadus_morhua', 'Microgadus_proximus', 'Microgadus_tomcod', 'Micromesistius_poutassou', 'Micromesistius_australis', 'Pollachius_virens']
new_lines = []

# load file and read line
in_file = open('Fish_tree.tre', 'r')
line = in_file.readline()
in_file.close()

# split into lines
lines = line.split(":")

# go through all variables and substitute
for item in fish:
	count = 0
	for line in lines:
		line = re.sub(item, item + "_" + str(count), line)
		new_lines.append(line)
		count += 1
	lines = new_lines
	new_lines = []

# join backup again with :'s
lines = ":".join(lines)

# write to new file
out_file = open('Fish_tree_new.tre', 'w')
out_file.write(str(lines) + "\n")
out_file.close()

# let user know we're finished
print "Done!"