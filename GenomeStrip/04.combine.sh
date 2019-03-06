#!/bin/sh
export tmp=/stor9000/apps/users/NWSUAF/2015060152/goat/tmp
export JAVA=/usr/bin
export ref=/stor9000/apps/users/NWSUAF/2015060152/bin/svtoolkit_database/1000G_phase3/human_g1k_hs37d5.fasta
export OUT=`pwd`
$JAVA/java -Xmx60g -Djava.io.tmpdir=$tmp -jar /stor9000/apps/appsoftware/BioSoftware/bin/GenomeAnalysisTK.jar \
        -R $ref \
        -T CombineVariants \
	--assumeIdenticalSamples \
        --variant ../chr1/deletion/chr1.genotypes.vcf \
        --variant ../chr1/duplication/genotypes.vcf \
	--variant ../chr2/deletion/chr2.genotypes.vcf \
	--variant ../chr2/duplication/chr2.dup.genotypes.vcf \
	--variant ../chr3/duplication/chr3.dup.genotypes.vcf \
	--variant ../chr3/deletion/chr3.genotypes.vcf \
	--variant ../chr4-5/deletion/chr4.genotypes.vcf \
 	--variant ../chr4-5/deletion/chr5.genotypes.vcf \
	--variant ../chr4-5/duplication/chr4-5.dup.genotypes.vcf \
	--variant ../chr6-7/deletion/chr6.genotypes.vcf \
	--variant ../chr6-7/deletion/chr7.genotypes.vcf \
	--variant ../chr6-7/duplication/chr6-7.dup.genotypes.vcf \
	--variant ../chr8-9/deletion/chr8.genotypes.vcf \
	--variant ../chr8-9/deletion/chr9.genotypes.vcf \
	--variant ../chr8-9/duplication/chr8-9.dup.genotypes.vcf \
	--variant ../chr10/deletion/chr10.genotypes.vcf \
	--variant ../chr10/deletion/chr11.genotypes.vcf \
	--variant ../chr10/deletion/chr12.genotypes.vcf \
	--variant ../chr10/duplication/chr10-12.dup.genotypes.vcf \
	--variant ../chr13-15/deletion/chr13.genotypes.vcf \
	--variant ../chr13-15/deletion/chr14.genotypes.vcf \
	--variant ../chr13-15/deletion/chr15.genotypes.vcf \
	--variant ../chr13-15/duplication/chr13-15.dup.genotype.vcf \
	--variant ../chr16-20/deletion/chr16.genotypes.vcf \
	--variant ../chr16-20/deletion/chr17.genotypes.vcf \
	--variant ../chr16-20/deletion/chr18.genotypes.vcf \
	--variant ../chr16-20/deletion/chr19.genotypes.vcf \
	--variant ../chr16-20/deletion/chr20.genotypes.vcf \
	--variant ../chr16-20/duplication/chr16.18.19.20.dup.genotype.vcf \
	--variant ../chr17/duplication/chr17.dup.genotypes.vcf \
	--variant ../chr21/deletion/chr21.genotypes.vcf \
	--variant ../chr21/duplication/chr21.dup.genotypes.vcf \
	--variant ../chr22/deletion/chr22.genotypes.vcf \
	--variant ../chr22/duplication/chr22.dup.genotypes.vcf \
	-o $OUT/genomestrip.raw'.vcf'
