#!/bin/bash

#If you adapt this script for your own use, you will need to set these two variables based on your environment.
export PATH=/stor9000/apps/appsoftware/BioSoftware/bin:/stor9000/apps/users/NWSUAF/2015060152/bin:$PATH
# SV_DIR is the installation directory for SVToolkit - it must be an exported environment variable.
# SV_TMPDIR is a directory for writing temp files, which may be large if you have a large data set.
export SV_DIR=/stor9000/apps/users/NWSUAF/2015060152/bin/svtoolkit



# These executables must be on your path.
which java > /dev/null || exit 1
which Rscript > /dev/null || exit 1
which samtools > /dev/null || exit 1

# For SVAltAlign, you must use the version of bwa compatible with Genome STRiP.
export PATH=${SV_DIR}/bwa:${PATH}
export LD_LIBRARY_PATH=${SV_DIR}/bwa:${LD_LIBRARY_PATH}

mx="-Xmx100g"
classpath="${SV_DIR}/lib/SVToolkit.jar:${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar:${SV_DIR}/lib/gatk/Queue.jar"


export REFDIR=/stor9000/apps/users/NWSUAF/2015060152/bin/svtoolkit_database/1000G_phase3

# Unzip the reference sequence and masks if necessary
if [ ! -e $REFDIR/human_g1k_hs37d5.fasta -a -e $REFDIR/human_g1k_hs37d5.fasta.gz ]; then
    gunzip $REFDIR/human_g1k_hs37d5.fasta.gz
fi
if [ ! -e $REFDIR/human_g1k_hs37d5.svmask.fasta -a -e $REFDIR/human_g1k_hs37d5.svmask.fasta.gz ]; then
    gunzip data/human_b36_chr1.svmask.fasta.gz
fi
if [ ! -e $REFDIR/human_g1k_hs37d5.gcmask.fasta -a -e $REFDIR/human_g1k_hs37d5.gcmask.fasta.gz ]; then
    gunzip $REFDIR/human_g1k_hs37d5.gcmask.fasta.gz
fi

# Display version information.
java -cp ${classpath} ${mx} -jar ${SV_DIR}/lib/SVToolkit.jar

# Run CNVDiscoveryPipeline
java -cp ${classpath} ${mx} \
     org.broadinstitute.sv.apps.GenerateHaploidCNVGenotypes \
     -R $REFDIR/human_g1k_hs37d5.fasta \
     -ploidyMapFile /stor9000/apps/users/NWSUAF/2015060152/bin/svtoolkit_database/1000G_phase3/human_g1k_hs37d5.ploidymap.txt \
     -genderMapFile /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip_whole_genome/gendermap \
     -vcf ./results/gs_cnv.genotypes.vcf.gz \
     -O chr13-15.dup.genotype.vcf \
     -estimateAlleleFrequencies true \
     -genotypeLikelihoodThreshold 0.001
