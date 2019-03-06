#!/bin/bash
if [ $# -ne 3 ]; then
 echo "error.. need args"
 echo "command:$0 <VCF> <database name> <database name>"
 exit 1
fi
VCF=$1
DatabaseName=$2
DatabasePath=$3
#echo -e "Chr\tPos\tPos\tRef\tAlt" > Anno.input
bcftools query -H -f '%CHROM\t%POS\t%POS\t%REF\t%ALT\n' ${VCF} >> Anno.input
#sheep
~/software/annovar/annotate_variation.pl -out Anno.out -build ${DatabaseName} Anno.input ${DatabasePath}
python3 ~/script/SnpCalling/Anno/annovar/SumAnno.py -i Anno.out.variant_function -o Sum.Result
