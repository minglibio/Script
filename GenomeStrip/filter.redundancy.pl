#!/usr/bin/perl
use strict;
use Data::Dumper;
die "Usage : perl $0 <Redundancy report table> <merge.vcf> <output>\n" unless @ARGV == 3;
open (IN1, "$ARGV[0]") or die "Redundancy report table required!\n";
open (IN2, "$ARGV[1]") or die "merge.vcf required!\n";
open (OUT, ">$ARGV[2]") or die "permission denied!\n";
my $header = <IN1>;
my %deletion;
while(<IN1>){
	chomp;
	my @inf = split/\s+/;
	if ($inf[0] eq $inf[-1]){
		$deletion{$inf[1]} = 1;
	}
	elsif ($inf[1] eq $inf[-1]){
		$deletion{$inf[0]} = 1;
	}
}
print STDERR Dumper\%deletion;
close IN1;
print STDERR "deleted region number:",scalar(keys %deletion),"\n";
while(<IN2>){
	chomp;
	if (/^#/){
		print OUT $_,"\n";
	}else{
		my @tmp = split/\t/;
		next if (exists $deletion{$tmp[2]});
		print OUT $_,"\n";
	}
}
close IN2;
close OUT;
