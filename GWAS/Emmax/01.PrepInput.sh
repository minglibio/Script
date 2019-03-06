#/bin/bash
if [ $# -ne 3 ]; then
 echo "error.. need args"
 echo "command:$0 <VCF file> <Output name> <autosome number>"
 exit 1
fi
VCF=$1
OUT=$2
CHR=$3
plink --vcf ${VCF} --output-missing-genotype 0 --geno 0.1 --maf 0.01 --recode 12 transpose --out ${OUT} --allow-extra-chr --chr-set ${CHR}
######### Add SNP IDs
cut -d " " -f5- ${OUT}.tped > ${OUT}.tped.tmp
cut -d " " -f1-4 ${OUT}.tped > ${OUT}.tped.headcol
awk '{print $1," ",$1,":",$4," ",$3," ",$4}' OFS="" ${OUT}.tped.headcol > ${OUT}.tped.headcol.tmp
paste -d " " ${OUT}.tped.headcol.tmp ${OUT}.tped.tmp > ${OUT}.tped
mv ${OUT}.tped.headcol.tmp ${OUT}.tped.headcol
rm ${OUT}.tped.tmp
#############
#cut -d " " -f1-4 ${OUT}.tped > ${OUT}.tped.headcol
emmax-kin -v -h -s -d 10 ${OUT}
