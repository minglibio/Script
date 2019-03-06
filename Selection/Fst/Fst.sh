#!/bin/bash
if [ $# -ne 4 ]; then
 echo "error.. need args"
 echo "command:$0 <VCF> <Pop1> <Pop2> <Out>"
 exit 1
fi
VCF=$1
Pop1=$2
Pop2=$3
Out=$4
vcftools --gzvcf ${VCF} --weir-fst-pop ${Pop1} --weir-fst-pop ${Pop2} --out ${Out} --max-missing 0.9 --maf 0.05
