from Bio import SeqIO

# setup file output names
fastq_in = "SRR006061.fastq"
qual_out = "SRR006061.qual"

# open file handles
fastq_fh = open(fastq_in, 'rU')
qual_fh = open(qual_out, 'w')

# setup fastq iterator
fastq_iterator = SeqIO.parse(fastq_fh, "fastq")

# output QUAL
print "Outputting QUAL..."
SeqIO.write(fastq_iterator, qual_fh, "qual")

# close file handles
qual_fh.close()
