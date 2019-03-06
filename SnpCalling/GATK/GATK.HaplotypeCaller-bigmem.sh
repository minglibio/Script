#/bin/bash
Region=$1
Name=$2
Ref=$3
SampleList=$4
CoreNum=$5
java -Xmx200g -Djava.io.tmpdir=/stor9000/apps/users/NWSUAF/2015050469/tmp -jar /stor9000/apps/users/NWSUAF/2015050469/software/GATK3.8/GenomeAnalysisTK.jar \
      -R ${Ref} \
      -I ${SampleList} \
      -T HaplotypeCaller \
      -o Sheep.${Name}.GATK.raw.vcf \
      --output_mode EMIT_VARIANTS_ONLY \
      -nct ${CoreNum} \
      --filter_mismatching_base_and_quals \
      -L ${Region} \
      --interval_padding 100
