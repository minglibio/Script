#!/usr/bin/perl
use strict;
die "Usage : perl $0 <Genomestrip table> <IRS dat> <IRS result vcf> <output>\n" unless @ARGV==4;
open (IN1, "$ARGV[0]") or die "Genomestrip table file required!\n";
open (IN2, "$ARGV[1]") or die "IRS dat file required\n";
open (IN3, "$ARGV[2]") or die "IRS result vcf required!\n";
open (OUT, ">$ARGV[3]") or die "permission denied!\n";
my %hash_cp;
my $header1 = <IN1>;
chomp $header1;
while(<IN1>){
	chomp;
	my @inf1 = split/\s+/;
	$hash_cp{$inf1[0].":".$inf1[1]} = $_;
}
close IN1;
my $header2 = <IN2>;
chomp $header2;
print OUT "$header1\t$header2\ttype\n";
my %hash_type;
while(<IN3>){
	next if /^#/;
	my @inf3 = split/\t/, $_;
	$inf3[4] =~ s/>//;
	$inf3[4] =~ s/<//;
	$hash_type{$inf3[2]}=$inf3[4];
}
close IN3;
while(<IN2>){
	chomp;
	my @inf2 = split/\t/;
	if (exists $hash_cp{$inf2[0]} and exists $hash_type{$inf2[0]}){
		print OUT "$hash_cp{$inf2[0]}\t$_\t$hash_type{$inf2[0]}\n";
	}
	else{
		print STDERR $_,"\n";
	}
}
close IN2;
close OUT;
