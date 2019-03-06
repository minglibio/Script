#!/bin/sh
if [ $# -ne 3 ]; then
 echo "error.. need args"
 echo "command:$0 <Input[vcf]> <chromosome list[e.g. {{1..26},X}]> <XML file> <Trait name>"
 exit 1
fi
IN=$1
#CHR=$2
XML=$2
Trait=$3
#for i in {{1..26},X}
plink --vcf ${IN} --make-bed --output-missing-genotype 0 --geno 0.1 --maf 0.1 --out Input --allow-extra-chr --chr-set 31
for i in {{1..29},X1,X2}
do
plink --bfile Input --recode --output-missing-genotype 0 --geno 0.1 --maf 0.1 --out Input.ts --allow-extra-chr --chr-set 31 --chr ${i}
~/script/GWAS/TASSEL/run_pipeline.pl -Xmx50g -configFile ${XML}
mv glm_out1.txt "glm_chr${i}_out1.txt"
done
cat glm_chr*_out1.txt >glm_total.txt
python3 ~/script/GWAS/TASSEL/Tassel2Plot.py -t ${Trait} -i glm_total.txt -o ${Trait}.assoc.plot.txt
Rscript ~/script/GWAS/manqqplot.r ${Trait}.assoc.plot.txt ${Trait}
