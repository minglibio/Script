#!/bin/bash
if [ $# -ne 3 ]; then
 echo "error.. need args"
 echo "command: $0 <Threads> <Reads.fasta.gz> <prefix>"
 exit 1
fi
######
wtdbg2="/stor9000/apps/users/NWSUAF/2015050469/software/wtdbg-2.2_x64_linux/wtdbg2"
wtpoa="/stor9000/apps/users/NWSUAF/2015050469/software/wtdbg-2.2_x64_linux/wtpoa-cns"
Threads=$1
RawReads=$2
prefix=$3
######  Get alignments, assemble long reads ;  70G reads using ~85G memory
${wtdbg2} -t ${Threads} -s sequel -i ${RawReads} -fo ${prefix}
######  Derive consensus; low memory ~1G
${wtpoa} -t ${Threads} -i ${prefix}.ctg.lay.gz -fo ${prefix}.ctg.lay.fa
python3 ~/script/PanGenome/StatGenome.py -i ${prefix}.ctg.lay.fa -o ${prefix}.ctg.lay.fa.stat  # Stat consensus
######  1st polish consensus; low memory, minimap2 ~6G, other ~1G
minimap2 -t ${Threads} -x map-pb -a ${prefix}.ctg.lay.fa ${RawReads} | samtools view -@ ${Threads} -Sb - > ${prefix}.ctg.lay.map.bam
samtools sort -@ ${Threads} ${prefix}.ctg.lay.map.bam -o ${prefix}.ctg.lay.map.srt.bam
samtools view -@ ${Threads} ${prefix}.ctg.lay.map.srt.bam | ${wtpoa} -t ${Threads} -d ${prefix}.ctg.lay.fa -i - -fo ${prefix}.ctg.lay.2nd.fa
python3 ~/script/PanGenome/StatGenome.py -i ${prefix}.ctg.lay.2nd.fa -o ${prefix}.ctg.lay.2nd.fa.stat
###### 2nd polish consensus; low memory, minimap2 ~6G, other ~1G
minimap2 -t ${Threads} -x map-pb -a ${prefix}.ctg.lay.2nd.fa ${RawReads} | samtools view -@ ${Threads} -Sb - > ${prefix}.ctg.lay.2nd.map.bam
samtools sort -@ ${Threads} ${prefix}.ctg.lay.2nd.map.bam -o ${prefix}.ctg.lay.2nd.map.srt.bam
samtools view -@ ${Threads} ${prefix}.ctg.lay.2nd.map.srt.bam | ${wtpoa} -t ${Threads} -d ${prefix}.ctg.lay.2nd.fa -i - -fo ${prefix}.ctg.lay.3th.fa
python3 ~/script/PanGenome/StatGenome.py -i ${prefix}.ctg.lay.3th.fa -o ${prefix}.ctg.lay.3th.fa.stat
###### 3th polish consensus; low memory, minimap2 ~6G, other ~1G
minimap2 -t ${Threads} -x map-pb -a ${prefix}.ctg.lay.3th.fa ${RawReads} | samtools view -@ ${Threads} -Sb - > ${prefix}.ctg.lay.3th.map.bam
samtools sort -@ ${Threads} ${prefix}.ctg.lay.3th.map.bam -o ${prefix}.ctg.lay.3th.map.srt.bam
samtools view -@ ${Threads} ${prefix}.ctg.lay.3th.map.srt.bam | ${wtpoa} -t ${Threads} -d ${prefix}.ctg.lay.3th.fa -i - -fo ${prefix}.ctg.lay.4th.fa
python3 ~/script/PanGenome/StatGenome.py -i ${prefix}.ctg.lay.4th.fa -o ${prefix}.ctg.lay.4th.fa.stat
###### Run BUSCO
mkdir busco
cd busco
bash ~/script/PanGenome/busco.sh ../${prefix}.ctg.lay.4th.fa
