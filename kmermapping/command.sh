bwa mem -t 20 -M -R '@RG\tID:kmer\tLB:kmer\tPL:ILLUMINA\tSM:kmer' ../hg19.fa test.fa | samtools view -bS - -o test.bwa.bam
blat -fastMap -minScore=100 -minIdentity=95 ~/database/pig/pig.fa kmer.fa kmer.psl
