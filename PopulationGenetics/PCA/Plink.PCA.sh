#/bin/bash
if [ $# -ne 3 ]; then
 echo "error.. need args"
 echo "command:$0 <VCF file> <Output name> <Sample list file [two-column]>"
 exit 1
fi
VCF=$1
OUT=$2
Sample=$3
#plink --vcf ${VCF} --pca --sheep --autosome --maf 0.0001 --out ${OUT} --keep ${Sample}
plink --vcf ${VCF} --pca --chr-set 29 --allow-extra-chr --autosome --maf 0.0001 --out ${OUT} --keep ${Sample}
