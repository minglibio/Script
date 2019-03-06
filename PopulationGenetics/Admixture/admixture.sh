#!/bin/sh
# generate random number: shuf -i 1-100 -n 1
if [ $# -ne 3 ]; then
 echo "error.. need args"
 echo "command: $0 <K> <seed> <Bed file>"
 exit 1
fi
K=$1
seed=$2
bed=$3
admixture -s ${seed} --cv ${bed} ${K} -j4 | tee log${K}.out
