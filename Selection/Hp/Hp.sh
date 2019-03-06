#!/bin/bash
if [ $# -ne 5 ]; then
 echo "error.. need args"
 echo "command:$0 <gzVCF> <Pop> <Win> <Step> <Out>"
 exit 1
fi
VCF=$1
Pop=$2
Win=$3
Step=$4
Out=$5
vcftools --gzvcf ${VCF} --keep ${Pop} --counts2 --out ${Out}
python3 ~/script/Selection/Hp/CalHpFromReadsCount.py -i ${Out}.frq.count -w ${Win} -s ${Step} -o ${Out}.${Win}K${Step}K.Hp
