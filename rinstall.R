# install all my favourite packages
install.packages(c("gdata", "zoo", "caTools", "ape", "picante", "phangorn", "adephylo", "ade4", "phytools", "phybase", "phyclust", "laser", "TreePar", "TreeSim", "MCMCglmm", "treebase", "rmesquite", "ggplot2", "plyr", "devtools", "rggobi"), dependencies=TRUE)

# install phylogenetics views
install.packages("ctv")
library("ctv")
install.views("Phylogenetics")

# bioconductor install
source("http://bioconductor.org/biocLite.R")
biocLite() # install some defaults

# install software packages
biocLite(c("AnnotationDbi", "bioMart", "Biostrings", "BSgenome", "ctc", "gene2pathway", "GeneAnswers", "geneplotter", "GeneR", "GenomeGraphs", "genomeIntervals", "genomes", "GenomicFeatures", "GenomicRanges", "Genominator", "GEOmetadb", "ggbio", "GLAD", "GOFunction", "goProfiles", "goTools", "gpls", "KEGGgraph", "keggorthology", "KEGGSOAP", "mBPCR", "mcaGUI", "ontoCAT", "ontoTools", "OrderedList", "OTUbase", "pcaMethods", "pcot2", "qtbase", "RBioinf", "Rsamtools", "Rsubread", "rtracklayer", "Rtreemix", "SBMLR", "ScISI", "SIM", "Streamer"))

# install AnnotationData - FunctionalAnnotation
biocLite(c("GO.db", "KEGG.db"))

# install AnnotationData - Organism
biocLite(c("BSgenome.Hsapiens.UCSC.hg19", "BSgenome.Ptroglodytes.UCSC.panTro2"))