#!/usr/bin/perl
use strict;
die "Usage: perl $0 <GenomeSTRIP gzvcf> <output>\n" unless @ARGV==2;
my $input = $ARGV[0];
open (IN,($input =~ /\.gz$/)? "gzip -dc $input |" : $input) or die "gzipped vcf file required!\n";
open (OUT, ">$ARGV[1]") or die "permission denied!\n";
my %hash;
print OUT "chr\tstart\tend\ttype\tfilter";
while(<IN>){
	next if /^##/;
	if (/^#CHR/){
		my @tmp_head = split/\s+/;
		for my $index (9..$#tmp_head){
			print OUT "\t$tmp_head[$index]";
		}
		for my $index (9..$#tmp_head){
			print OUT "\t$tmp_head[$index]";
		}
		print OUT "\n";
	}
	else{
		chomp;
		my @tmp = split/\s+/;
		my $end;
		if ($tmp[7] =~ /;END=(\d+)/){
			$end = $1;
		}
		elsif ($tmp[7] =~ /^END=(\d+)/){
			$end = $1;
		}
		else{
			print STDERR "something error!\n";
		}
		my ($svtype) = $tmp[7] =~ /SVTYPE=([a-zA-Z]+)/;
		if ($svtype eq "CNV"){
			($svtype) = $tmp[7] =~ /GSCNCATEGORY=([a-zA-Z]+)/;
		}
		print OUT $tmp[0],"\t",$tmp[1],"\t",$end,"\t",$svtype,"\t",$tmp[6],"\t";
		my @genotype_array;
		my @cp_array;
		for my $index(9..$#tmp){
			my ($genotype,$cp) = (split/:/,$tmp[$index])[0,1];
			push @genotype_array, $genotype;
			push @cp_array, $cp;
		}
		print OUT join("\t",@genotype_array),"\t",join("\t",@cp_array),"\n";
	}
}
close IN;
close OUT;
