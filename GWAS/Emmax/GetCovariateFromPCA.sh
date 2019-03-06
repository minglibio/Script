#/bin/bash
if [ $# -ne 1 ]; then
 echo "error.. need args"
 echo "command:$0 <PCA file[eigenvec]>"
 exit 1
fi
IN=$1
awk '{print $1,$2,1,$3,$4,$5,$6,$7}' OFS="\t" ${IN} > covariate
