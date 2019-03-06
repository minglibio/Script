#!/bin/bash
if [ $# -ne 5 ]; then
 echo "error.. need args"
 echo "command: $0 <Ref fasta file> <Fasta file> <Prefix> <BlastDB> <Threads>"
 exit 1
fi
###### Argument 
Ref=$1   # /stor9000/apps/users/NWSUAF/2015050469/Ref/Chicken/GRCg6a/GCF_000002315.5_GRCg6a_rename.fa
Assembly=$2  # /stor9000/apps/users/NWSUAF/2015050469/02.Chicken/06.PanGenome/01.Data/02.Assembly/NGS/chicken-wuji-scaffolds-v1.0.fasta
Prefix=$3  # wuji
BlastDB=$4 # ~/Ref/Chicken/GRCg6a/blast/GRCg6a
Threads=$5
###### Align de novo assembly to reference
minimap2 -t ${Threads} -cx asm10 ${Ref} ${Assembly} > ${Prefix}.paf
###### Stat length of each contig and gap of de novo assembly 
python3 ~/script/PanGenome/StatChrLenAndN.py -i ${Assembly} -o ${Prefix}
###### Trans alignment to bed format
awk '{print $1,$3,$4}' OFS="\t" ${Prefix}.paf > ${Prefix}.paf.bed
###### Extract unmap region of de novo assembly
bedtools subtract -nonamecheck -a ${Prefix}.bed -b ${Prefix}.paf.bed > ${Prefix}.unmap
###### Remove gap of unmap region
bedtools subtract -nonamecheck -a ${Prefix}.unmap -b ${Prefix}.N.bed > ${Prefix}.unmap.rmN.tmp
###### Merge unmap region within 200 bp
bedtools merge -d 200 -i ${Prefix}.unmap.rmN.tmp > ${Prefix}.unmap.rmN
#bedtools merge -d 200 -i ${Prefix}.unmap.rmN.tmp |awk '$3-$2>=500' > ${Prefix}.unmap.rmN
rm ${Prefix}.unmap.rmN.tmp
###### Get seqence of unmap region
bedtools getfasta -fi ${Assembly} -bed ${Prefix}.unmap.rmN -fo ${Prefix}.unmap.rmN.fa
######  Blast ~1-3h; Local alignment to reference
blastn -task blastn -db ${BlastDB} -query ${Prefix}.unmap.rmN.fa -out ${Prefix}.unmap.rmN.blastout -num_threads ${Threads} -word_size 20 -max_hsps 1 -max_target_seqs 1 -dust no -soft_masking false -evalue 0.00001 -outfmt "6 qseqid sseqid pident qlen length mismatch gapopen qstart qend sstart send evalue bitscore qcovs"
###### Extract region which identity ＞ 90%
python3 ~/script/PanGenome/TransBlast2Bed.py -i ${Prefix}.unmap.rmN.blastout -o ${Prefix}.unmap.rmN.blastout.bed
###### Remove region which identity ＞90% from unmap region
bedtools subtract -nonamecheck -a ${Prefix}.unmap.rmN -b ${Prefix}.unmap.rmN.blastout.bed > ${Prefix}.unmap.rmN.rmBlast
###### Merge unmap region and remove region which length less than 500 bp
bedtools merge -d 200 -i ${Prefix}.unmap.rmN.rmBlast > ${Prefix}.unmap.rmN.rmBlast.merge
#bedtools merge -d 200 -i ${Prefix}.unmap.rmN.rmBlast |awk '$3-$2>=500' > ${Prefix}.unmap.rmN.rmBlast.merge
###### Get seqence of unmap region
bedtools getfasta -fi ${Assembly} -bed ${Prefix}.unmap.rmN.rmBlast.merge -fo ${Prefix}.unmap.rmN.rmBlast.merge.fa.tmp
###### remove region which length less than 500 bp
python3 ~/script/PanGenome/FilterSeq.py -i ${Prefix}.unmap.rmN.rmBlast.merge.fa.tmp -o ${Prefix}.unmap.rmN.rmBlast.merge.fa
rm ${Prefix}.unmap.rmN.rmBlast.merge.fa.tmp
###### Change name of contigs
sed -i s/\>/\>${Prefix}#/g ${Prefix}.unmap.rmN.rmBlast.merge.fa
###### Stat novel sequence
python3 ~/script/PanGenome/StatGenome.py -i ${Prefix}.unmap.rmN.rmBlast.merge.fa -o ${Prefix}.unmap.rmN.rmBlast.merge.stat
