#!/bin/sh
export dir=$1
for a in `cat $dir`
do
echo -n  $a
cd ./$a
for i in `cat /stor9000/apps/users/NWSUAF/2012010954/DuDuo/Y_new_pan/goat_ran/pangenome_ASR/GATK/gvcf/shell/10X/shellID_all`
do
  #cd $a
  if [ ! -f "$i.g.vcf.gz.tbi" ]; then
      echo -n "  $i  "
  fi
 done
  cd ..
  echo 
done
