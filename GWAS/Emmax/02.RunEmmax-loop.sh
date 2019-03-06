#!/bin/sh
if [ $# -ne 3 ]; then
  echo "error.. need args"
  echo "command:$0 <> <> <>"
  exit 1
fi

for (( d=3; d<=4; d++ ))
do
n=$[$d-2]
cut -f1-2,$d Trait >'T'$n'.txt'
emmax -v -d 10 -t Hybrid -p 'T'$n'.txt' -k Hybrid.hIBS.kinf -c covariate -o 'gwas.T'$n
paste Hybrid.tped.headcol 'gwas.T'$n'.ps' >'gwas.T'$n'.result.txt'
awk '{$3=null;$5=null;$6=null;print}' 'gwas.T'$n'.result.txt' >'gwas.T'$n'.assoc.txt'
sed -i '1i\CHR SNPID BP P' 'gwas.T'$n'.assoc.txt'
perl emmaxfilter.pl 'gwas.T'$n'.assoc.txt' 'gwas.T'$n'.assoc.plot.txt'
done
perl emmaxPlot.pl
