#!/usr/bin/perl -w
use strict;
die "Usage: perl $0 <chromosome level ID> <bam list absolute path> <ref> <output>\n" unless @ARGV == 4;
open (IN1, "$ARGV[0]") or die "chromosome levels ID missing!\n";
open (IN2, "$ARGV[1]") or die "absolute path bam list missing!\n";
my %chr;
while(<IN1>){
	chomp;
	$chr{$_} = 1;
}
close IN1;
while(<IN2>){
	next if /^#/;
	chomp;
	my $bam = $_;
	my @tmp = split/\//, $_;
	my $sample = (split/\./, $tmp[-1])[0];
	system "mkdir -p $ARGV[3]/$sample";
	die "file $ARGV[3]/$sample/scaffold_chr.sh exists\n" if (-e "$ARGV[3]/$sample/scaffold_chr.sh");
	die "file $ARGV[3]/$sample/novel_chr.sh exists\n" if (-e "$ARGV[3]/$sample/novel_chr.sh");
	open (SCA1, ">>$ARGV[3]/$sample/novel_chr.sh") or die "permission denied!\n";
	open (SCA2, ">>$ARGV[3]/$sample/scaffold_chr.sh") or die "permission denied!\n";
	print SCA1 "#!/bin/sh\n/stor9000/apps/appsoftware/BioSoftware/bin/java -Xmx40g -Djava.io.tmpdir=/stor9000/apps/users/NWSUAF/2012010954/temp -jar /stor9000/apps/users/NWSUAF/2015060152/bin/GATK3.7/GenomeAnalysisTK.jar -R $ARGV[2] -T HaplotypeCaller -L /stor9000/apps/users/NWSUAF/2012010954/DuDuo/Y_new_pan/goat_ran/pangenome_ASR/GATK/gvcf/shell/novelID.list  -ERC GVCF -I $bam -o novel.g.vcf.gz\n";
	print SCA2 "#!/bin/sh\n/stor9000/apps/appsoftware/BioSoftware/bin/java -Xmx40g -Djava.io.tmpdir=/stor9000/apps/users/NWSUAF/2012010954/temp -jar /stor9000/apps/users/NWSUAF/2015060152/bin/GATK3.7/GenomeAnalysisTK.jar -R $ARGV[2] -T HaplotypeCaller -L /stor9000/apps/users/NWSUAF/2012010954/DuDuo/Y_new_pan/goat_ran/pangenome_ASR/GATK/gvcf/shell/scaffoldID.list  -ERC GVCF -I $bam -o scaffold.g.vcf.gz\n";
	foreach my $chr (sort {$a cmp $b}  keys %chr){
		die "file $ARGV[3]/$sample/chr.sh exists\n" if (-e "$ARGV[3]/$sample/$chr.sh");
		open (OUT, ">$ARGV[3]/$sample/$chr.sh") or die "permission denied!\n";
		print OUT "#!/bin/sh\n";
		print OUT "/stor9000/apps/appsoftware/BioSoftware/bin/java -Xmx40g -Djava.io.tmpdir=/stor9000/apps/users/NWSUAF/2012010954/temp -jar /stor9000/apps/users/NWSUAF/2015060152/bin/GATK3.7/GenomeAnalysisTK.jar -R $ARGV[2] -T HaplotypeCaller -L $chr -ERC GVCF -I $bam -o $chr.g.vcf.gz\n";
		#print SCA " -XL $chr";
	}
	#print SCA1 "-L /stor9000/apps/users/NWSUAF/2012010954/DuDuo/Y_new_pan/goat_ran/pangenome_ASR/GATK/gvcf/shell/novelID.list  -ERC GVCF -I $bam -o novel.g.vcf.gz\n"
	#print SCA2 "-L /stor9000/apps/users/NWSUAF/2012010954/DuDuo/Y_new_pan/goat_ran/pangenome_ASR/GATK/gvcf/shell/scaffoldID.list  -ERC GVCF -I $bam -o scaffold.g.vcf.gz\n"
}
close IN2;
