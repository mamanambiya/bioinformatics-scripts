#import entrez module
import sys
from Bio import Entrez

# get arguments
args = sys.argv[1:]

# check input arguments
if len(args) < 1:
	print "Expect at least one tax id as an input argument"
	sys.exit()

# set variables
#taxids = [515482, 515474]
taxids = args

# set email
Entrez.email = "gawbul@gmail.com"

# traverse ids
for taxid in taxids:
	handle = Entrez.efetch(db="taxonomy", id=taxid, mode="text", rettype="xml")
	records = Entrez.read(handle)
	for taxon in records:
		taxid = taxon["TaxId"]
		name = taxon["ScientificName"]
		tids = []
		for t in taxon["LineageEx"]:
			tids.insert(0, t["TaxId"])
		tids.insert(0, taxid)
		print "%s\t|\t%s\t|\t%s" % (taxid, name, " ".join(tids))