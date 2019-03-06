#!/bin/sh
if [ $# -ne 3 ]; then
 echo "error.. need args"
 echo "command: $0 <rep number> <seed> <Bed file>"
 exit 1
fi
run=$1
seed=$2
bed=$3
mkdir -p ${run}.Rep || exit 1
cd ${run}.Rep
for i in {2..7}
do
jsub -R "rusage[res=1]span[hosts=1]" -q jynodequeue -e ${i}.e -o ${i}.o -n 20 -M 100000000 -J ${run}.Rep "bash ~/script/PopulationGenetics/Admixture/admixture.sh ${i} ${seed} ${bed}"
done
