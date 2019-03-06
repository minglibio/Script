#!/bin/bash

#If you adapt this script for your own use, you will need to set these two variables based on your environment.
export PATH=/stor9000/apps/appsoftware/BioSoftware/bin:/stor9000/apps/users/NWSUAF/2015060152/bin:$PATH
# SV_DIR is the installation directory for SVToolkit - it must be an exported environment variable.
# SV_TMPDIR is a directory for writing temp files, which may be large if you have a large data set.
export SV_DIR=/stor9000/apps/users/NWSUAF/2015060152/bin/svtoolkit

SV_TMPDI=`pwd`
runDir=`pwd`


# These executables must be on your path.
which java > /dev/null || exit 1
which Rscript > /dev/null || exit 1
which samtools > /dev/null || exit 1

# For SVAltAlign, you must use the version of bwa compatible with Genome STRiP.
export PATH=${SV_DIR}/bwa:${PATH}
export LD_LIBRARY_PATH=${SV_DIR}/bwa:${LD_LIBRARY_PATH}

mx="-Xmx100g"
classpath="${SV_DIR}/lib/SVToolkit.jar:${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar:${SV_DIR}/lib/gatk/Queue.jar"

mkdir -p ${runDir}/logs || exit 1
mkdir -p ${runDir}/metadata || exit 1
mkdir -p ${SV_TMPDI}/tmp || exit 1

export REFDIR=/stor9000/apps/users/NWSUAF/2015060152/bin/svtoolkit_database/1000G_phase3

# Unzip the reference sequence and masks if necessary
if [ ! -e $REFDIR/human_g1k_hs37d5.fasta -a -e $REFDIR/human_g1k_hs37d5.fasta.gz ]; then
    gunzip $REFDIR/human_g1k_hs37d5.fasta.gz
fi
if [ ! -e $REFDIR/human_g1k_hs37d5.svmask.fasta -a -e $REFDIR/human_g1k_hs37d5.svmask.fasta.gz ]; then
    gunzip $REFDIR/human_g1k_hs37d5.svmask.fasta.gz
fi
if [ ! -e $REFDIR/human_g1k_hs37d5.gcmask.fasta -a -e $REFDIR/human_g1k_hs37d5.gcmask.fasta.gz ]; then
    gunzip $REFDIR/human_g1k_hs37d5.gcmask.fasta.gz
fi

# Display version information.
java -cp ${classpath} ${mx} -jar ${SV_DIR}/lib/SVToolkit.jar

# Run CNVDiscoveryPipeline
java -cp ${classpath} ${mx} \
    org.broadinstitute.gatk.queue.QCommandLine \
    -S ${SV_DIR}/qscript/discovery/cnv/CNVDiscoveryPipeline.q \
    -S ${SV_DIR}/qscript/SVQScript.q \
    -gatk ${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar \
    -cp ${classpath} \
    -tempDir ${SV_TMPDIR}/tmp \
    -configFile /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip_whole_genome/genstrip_parameters.txt \
    -R $REFDIR/human_g1k_hs37d5.fasta \
    -genderMapFile /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip_whole_genome/gendermap \
    -runDirectory ${runDir} \
    -md ../deletion/metadata \
    -jobLogDir ${runDir}/logs \
    -I /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip_whole_genome/bam.list \
    -intervalList chr13-15.list \
    -jobRunner Shell -gatkJobRunner Shell -tilingWindowSize 5000 \
    -tilingWindowOverlap 2500 -maximumReferenceGapLength 2500 -boundaryPrecision 200 -minimumRefinedLength 2500 -run \
    || exit 1
#-intervalList /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip/duplication/chr.list
