#!/bin/bash
Chr=$1
CoreNum=$2
java -Xmx100g -jar /stor9000/apps/users/NWSUAF/2015050469/software/GATK3.8/GenomeAnalysisTK.jar \
    --num_threads ${CoreNum} \
    --reference_sequence /stor9000/apps/users/NWSUAF/2015050469/Ref/Sheep/OAR4.0/GCF_000298735.2_Oar_v4.0_genomic_rename.fna \
    --analysis_type SelectVariants \
    --variant Sheep.${Chr}.GATK.raw.vcf \
    --out Sheep.${Chr}.GATK.flt.vcf \
    --selectTypeToInclude SNP \
    --restrictAllelesTo BIALLELIC \
    --selectexpressions "AF < 1.00 && QUAL >= 30 && QD >= 2.0 && MQ >= 40.0 && MQRankSum >= -12.5 && ReadPosRankSum >= -8.0"
