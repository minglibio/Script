#!/bin/sh
if [ $# -ne 4 ]; then
  echo "error.. need args"
  echo "command:$0 <Input> <Trait file> <covariate file> <output>"
  exit 1
fi
IN=$1
Trait=$2
covariate=$3
OUT=$4
#emmax -v -d 10 -t ${IN} -p ${Trait} -k ${IN}.hIBS.kinf -c ${covariate} -o ${OUT}
emmax -v -d 10 -t ${IN} -p ${Trait} -k ${IN}.hIBS.kinf -o ${OUT}
paste ${IN}.tped.headcol ${OUT}.ps > ${OUT}.result.txt
awk '{$3=null;$5=null;$6=null;print}' ${OUT}.result.txt > ${OUT}.assoc.txt
sed -i '1i\CHR SNPID BP P' ${OUT}.assoc.txt
python3 ~/script/GWAS/Emmax/EmmaxFilter.py -i ${OUT}.assoc.txt -o ${OUT}.assoc.plot.txt
Rscript ~/script/GWAS/manqqplot.r ${OUT}.assoc.plot.txt ${OUT}
