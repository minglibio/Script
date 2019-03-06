#!/usr/bin/perl
use strict;
die "Usage : perl $0 <mdist.id> <mdist> <individual number> <out prefix>\n" unless @ARGV==4;
open(IN1, "$ARGV[0]") or die "mdist.id file required!\n";
open(IN2, "$ARGV[1]") or die "mdist file required!\n";
open(OUT, ">$ARGV[3]\.dist") or die "permission denied!\n";
print OUT "#nexus\nbegin taxa;\n dimensions ntax=$ARGV[2];\n taxlabels";
my $individual = 0;
my %hash;
while(<IN1>){
	chomp;
	$individual++;
	my @ind = split/\s+/;
	$hash{$individual} = $ind[0];
	print OUT " $ind[0]";
}
die "something wrong with the individual number!\n" unless $individual eq $ARGV[2];
print OUT ";\nend;\nbegin distances;\n dimensions ntax=$ARGV[2];\n format diagonal labels triangle=lower;\n matrix\n";
my $index = 0;
while(<IN2>){
	chomp;
	$index++;
	my @dis = split/\s+/;
	print OUT "  $hash{$index}";
	foreach my $tmp (0..($index-1)){
		print OUT " $dis[$tmp]";
	}
	print OUT "\n";
}
print OUT "  ;\nend;";
close OUT;
close IN2;
