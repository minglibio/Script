#!/bin/sh
export SV_DIR=/stor9000/apps/users/NWSUAF/2015060152/bin/svtoolkit
export LD_LIBRARY_PATH=/stor9000/apps/users/NWSUAF/2015060152/bin/svtoolkit/bwa:${LD_LIBRARY_PATH}
classpath="${SV_DIR}/lib/SVToolkit.jar:${SV_DIR}/lib/gatk/GenomeAnalysisTK.jar:${SV_DIR}/lib/gatk/Queue.jar"
mx="-Xmx40g"
chroms=`cat chr | cut -f 1`
for chr in ${chroms}
do
java -cp ${classpath} ${mx} org.broadinstitute.sv.apps.ComputeGenomeMask -R ASM.fa  -O `pwd`/${chr}.fasta -readLength 36 -sequence ${chr}
python /stor9000/apps/users/NWSUAF/2015060152/script/GenomeStrip/softmasked_to_bed.py ${chr}.fasta >${chr}.alignable.region
done
