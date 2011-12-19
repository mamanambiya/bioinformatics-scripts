# import modules
import sys, os, glob

# get input arguments
if len(sys.argv) <= 2:
	print "No path argument given"
	sys.exit()
else:
	cwd = sys.argv[1]
	type = sys.argv[2]

# get all files in current directory
print "Getting all %s files from %s..." % (type, cwd)

# traverse files list
for file in glob.glob(os.path.join(cwd, '*.*')):
	path = os.path.join(cwd, file)
	inputfile = open(path, "r")
	count = 0
	while count <= 4:
		headers = inputfile.readline()
		count += 1
	lines = inputfile.read()
	for line in lines:
		fastaseq.append(line.strip())
	inputfile.close()
	fileparts = split(".", file)
	path = os.path.join(cwd, fileparts[0] + ".fasta")
	outputfile = open(path, "w")
	outputfile.write(">" + fileparts[0] + "\n")
	for fastaline in fastaseq:
		outputfile.write(fastaline + "\n")
	outputfile.close()