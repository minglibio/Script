#/bin/bash
if [ $# -ne 1 ]; then
 echo "error.. need args"
 echo "command:$0 <PCA file[eigenvec]>"
 exit 1
fi
IN=$1
:>covariate
echo -e "<Trait>\tPC1\tPC2\tPC3\tPC4\tPC5" > covariate
awk '{print $2,$3,$4,$5,$6,$7}' OFS="\t" ${IN} >> covariate
