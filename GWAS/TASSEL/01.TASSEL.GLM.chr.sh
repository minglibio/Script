#!/bin/sh
if [ $# -ne 3 ]; then
 echo "error.. need args"
 echo "command:$0 <Input[vcf]> <chromosome> <XML file>"
 exit 1
fi
IN=$1
CHR=$2
XML=$3
plink --file ${IN} --recode --output-missing-genotype 0 --maf 0.05 --out Input.ts --allow-extra-chr --chr-set 31 --chr ${CHR}
~/script/GWAS/TASSEL/run_pipeline.pl -Xmx100g -configFile ${XML}
mv glm_out1.txt "glm_chr${CHR}_out1.txt"
