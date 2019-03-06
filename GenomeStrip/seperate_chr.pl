#!/usr/bin/perl
use strict;
die "Usage : perl $0 <genome VCF> <chromosome ID>\n" unless @ARGV == 2;
open (IN, "$ARGV[0]") or die "vcf file required\n";
open (OUT, ">$ARGV[1].vcf") or die "permission denied\n";
while(<IN>){
	chomp;
	if (/^#/){
		print OUT $_,"\n";
	}else{
		my @tmp_array = split/\s+/;
		print OUT $_,"\n" if ($tmp_array[0] eq "$ARGV[1]");
	}
}
close IN;
close OUT;
