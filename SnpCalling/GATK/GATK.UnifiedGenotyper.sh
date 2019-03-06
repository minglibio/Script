#/bin/bash
Region=$1
Name=$2
Ref=$3
SampleList=$4
CoreNum=$5
java  -jar /stor9000/apps/users/NWSUAF/2015050469/software/GATK3.8/GenomeAnalysisTK.jar \
      -R ${Ref} \
      -I ${SampleList} \
      -T UnifiedGenotyper \
      -o Sheep.${Name}.GATK.raw.vcf \
      --output_mode EMIT_VARIANTS_ONLY \
      -nct ${CoreNum} \
      -glm SNP \
      --filter_mismatching_base_and_quals \
      -L ${Region} \
      --interval_padding 100
