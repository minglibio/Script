#!/bin/bash
export PATH=/stor9000/apps/appsoftware/BioSoftware/bin:$PATH
# If you adapt this script for your own use, you will need to set these two variables based on your environment.
# SV_DIR is the installation directory for SVToolkit - it must be an exported environment variable.
# SV_TMPDIR is a directory for writing temp files, which may be large if you have a large data set.
export SV_DIR=/stor9000/apps/users/NWSUAF/2015060152/bin/svtoolkit
export IN=`pwd`
export OUT=`pwd`

# These executables must be on your path.
# For SVAltAlign, you must use the version of bwa compatible with Genome STRiP.
export PATH=${SV_DIR}/bwa:${PATH}
export LD_LIBRARY_PATH=${SV_DIR}/bwa:${LD_LIBRARY_PATH}

mx="-Xmx40g"
classpath="${SV_DIR}/lib/SVToolkit.jar:${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar:${SV_DIR}/lib/gatk/Queue.jar"


# Unzip the reference sequence and masks if necessary
java -cp ${classpath} ${mx} -jar ${SV_DIR}/lib/SVToolkit.jar

# Run preprocessing.
# For large scale use, you should use -reduceInsertSizeDistributions, but this is too slow for the installation test.
# The method employed by -computeGCProfiles requires a GC mask and is currently only supported for human genomes.
for i in {1..5}
do
perl seperate_chr.pl $IN/IRS.vcf $i
java -cp ${classpath} ${mx} \
    org.broadinstitute.sv.main.SVAnnotator \
    -A IntensityRankSum \
    -R /stor9000/apps/users/NWSUAF/2015060152/bin/svtoolkit_database/1000G_phase3/human_g1k_hs37d5.fasta \
    -vcf $i.vcf \
    -O $OUT/$i.result.vcf \
    -arrayIntensityFile /stor9000/apps/users/NWSUAF/2015060152/bin/IRSTEST_database/ALL.genome.Affy6_probe_intensity_matrix_2506samples.20120621.dat \
    -irsUseGenotypes true \
    -writeReport true \
    -reportFile $OUT/$i.dat
echo $i "finished" 
done
