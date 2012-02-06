from Bio import SeqIO

# setup file output names
fastq_in = "SRR006061.fastq"
fasta_out = "SRR006061.fasta"

# open file handles
fastq_fh = open(fastq_in, 'rU')
fasta_fh = open(fasta_out, 'w')

# setup fastq iterator
fastq_iterator = SeqIO.parse(fastq_fh, "fastq")

# output FASTA
print "Outputting FASTA..."
SeqIO.write(fastq_iterator, fasta_fh, "fasta")

# close file handles
fasta_fh.close()

