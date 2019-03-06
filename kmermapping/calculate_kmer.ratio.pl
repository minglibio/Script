#!/usr/bin/perl
use strict;
die "Usage: perl $0 <kmer> <output>\n" unless @ARGV == 2;
my $kmerfile = &FastaReader($ARGV[0]) or die "kmer fasta file is required!\n";
print STDERR "kmer fasta loading finished!\n";
open (OUT, ">$ARGV[1]") or die "permission denied!\n";
foreach my $head (sort {$a <=> $b} keys %{$kmerfile}){
	my $a = $kmerfile->{$head} =~ tr/0/0/;
	my $b = $kmerfile->{$head} =~ tr/1/1/;
	my $c = $kmerfile->{$head} =~ tr/2/2/;
	my $e = $kmerfile->{$head} =~ tr/3/3/;
	my $f = $kmerfile->{$head} =~ tr/4/4/;
	my $g = $kmerfile->{$head} =~ tr/5/5/;
	my $h = $kmerfile->{$head} =~ tr/6/6/;
	my $i = $kmerfile->{$head} =~ tr/7/7/;
	my $j = $kmerfile->{$head} =~ tr/8/8/;
	my $k = $kmerfile->{$head} =~ tr/9/9/;
	my $l = $kmerfile->{$head} =~ tr/M/M/;
	print OUT $head,"\t",$a,"\t",$b,"\t",$c,"\t",$e,"\t",$f,"\t",$g,"\t",$h,"\t",$i,"\t",$j,"\t",$k,"\t",$l,"\n";
}
close IN;
close OUT;	
sub FastaReader {
	my ($file) = @_;
	open IN, "<", $file or die "Fail to open file: $file!\n";
	local $/ = '>';
	<IN>;
	my ($head, $seq, %hash);
	while (<IN>){
		s/\r?\n>?$//;
		( $head, $seq ) = split /\r?\n/, $_, 2;
		$seq =~ s/\s+//g;
		$hash{(split /\s+/,$head)[0]} = $seq;
	}
	close IN;
	$/ = "\n";
	return \%hash;
}

