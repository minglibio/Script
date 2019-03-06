#!/bin/bash

#If you adapt this script for your own use, you will need to set these two variables based on your environment.
export PATH=/stor9000/apps/appsoftware/BioSoftware/bin:/stor9000/apps/users/NWSUAF/2015060152/bin:$PATH
# SV_DIR is the installation directory for SVToolkit - it must be an exported environment variable.
# SV_TMPDIR is a directory for writing temp files, which may be large if you have a large data set.
export SV_DIR=/stor9000/apps/users/NWSUAF/2015060152/bin/svtoolkit

SV_TMPDIR=`pwd`
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
mkdir -p $SV_TMPDIR/tmp || exit 1

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

# Run preprocessing.
# For large scale use, you should use -reduceInsertSizeDistributions, but this is too slow for the installation test.
# The method employed by -computeGCProfiles requires a GC mask and is currently only supported for human genomes.
java -cp ${classpath} ${mx} \
    org.broadinstitute.gatk.queue.QCommandLine \
    -S ${SV_DIR}/qscript/SVPreprocess.q \
    -S ${SV_DIR}/qscript/SVQScript.q \
    -gatk ${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar \
    --disableJobReport \
    -cp ${classpath} \
    -configFile /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip_whole_genome/genstrip_parameters.txt \
    -tempDir ${SV_TMPDIR}/tmp \
    -R $REFDIR/human_g1k_hs37d5.fasta \
    -genderMapFile /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip_whole_genome/gendermap \
    -runDirectory ${runDir} \
    -md ${runDir}/metadata \
    -L 13 \
    -L 14 \
    -L 15 \
    -reduceInsertSizeDistributions true \
    -computeGCProfiles true \
    -computeReadCounts true \
    -jobLogDir ${runDir}/logs \
    -I /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip_whole_genome/bam.list \
    -run \
    || exit 1
for i in {13..15}
do
sites=chr$i.discovery.vcf
genotypes=chr$i.genotypes.vcf
#run discovery
java -cp ${classpath} ${mx} \
    org.broadinstitute.gatk.queue.QCommandLine \
    -S ${SV_DIR}/qscript/SVDiscovery.q \
    -S ${SV_DIR}/qscript/SVQScript.q \
    -gatk ${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar \
    --disableJobReport \
    -cp ${classpath} \
    -configFile /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip_whole_genome/genstrip_parameters.txt \
    -tempDir ${SV_TMPDIR}/tmp \
    -R $REFDIR/human_g1k_hs37d5.fasta \
    -genderMapFile /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip_whole_genome/gendermap \
    -runDirectory ${runDir} \
    -md ${runDir}/metadata \
    -jobLogDir ${runDir}/logs \
    -L $i \
    -minimumSize 100 \
    -maximumSize 3000000 \
    -suppressVCFCommandLines \
    -I /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip_whole_genome/bam.list \
    -O ${runDir}/${sites} \
    -run \
    || exit 1

# Run genotyping on the discovered sites.
java -cp ${classpath} ${mx} \
    org.broadinstitute.gatk.queue.QCommandLine \
    -S ${SV_DIR}/qscript/SVGenotyper.q \
    -S ${SV_DIR}/qscript/SVQScript.q \
    -gatk ${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar \
    --disableJobReport \
    -cp ${classpath} \
    -configFile /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip_whole_genome/genstrip_parameters.txt \
    -tempDir ${SV_TMPDIR}/tmp \
    -R $REFDIR/human_g1k_hs37d5.fasta \
    -genderMapFile /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip_whole_genome/gendermap \
    -runDirectory ${runDir} \
    -md ${runDir}/metadata \
    -jobLogDir ${runDir}/logs \
    -I /stor9000/apps/users/NWSUAF/2015060152/human/GenomeStrip_whole_genome/bam.list \
    -vcf ${runDir}/${sites} \
    -O ${runDir}/${genotypes} \
    -run \
    || exit 1
done
