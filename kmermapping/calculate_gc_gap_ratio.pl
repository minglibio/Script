#!/usr/bin/perl
use strict;
use Data::Dumper;
die "Usage: perl $0 <ref> <kmer> <CNVR> <output>\n" unless @ARGV == 4;
my $reffile = &FastaReader($ARGV[0]) or die "reference fasta file is required!\n";
my $mapfile = &FastaReader($ARGV[1]) or die "kmer fasta file is required!\n";
print STDERR "ref loading finished!\n";
open (IN, "$ARGV[2]") or die "CNVR required!\n";
open (OUT, ">$ARGV[3]") or die "permission denied!\n";
#my $header = <IN>;
#chomp $header;
#print OUT $header,"\t","gc_ratio","\t","repeat_ratio","\t","gap_ratio","\n";
while (<IN>){
	chomp;
	my @tmp = split /\t/;
	my $CNV_length = $tmp[2]-$tmp[1]+1;
	my $sub_seq = substr ($reffile->{$tmp[0]}, $tmp[1], $CNV_length);
	my $sub_kmer = substr ($mapfile->{$tmp[0]}, $tmp[1], $CNV_length);
	my $GC_count = () = $sub_seq =~ /[GC]/gi;
	my $gap = () = $sub_seq =~/N/gi;
	my $repeat_count = () = $sub_seq =~ /[atgc]/g ;
	my $GC_ratio = $CNV_length-$gap > 0 ? sprintf "%.2f", $GC_count/($CNV_length-$gap) : 0;
	my $gap_ratio = $CNV_length > 0 ? sprintf "%.2f", $gap/$CNV_length : 0;
	my $repeat_ratio = $CNV_length-$gap > 0 ? sprintf "%.2f", $repeat_count/($CNV_length-$gap) : 0;
	my $a = $sub_kmer =~ tr/0/0/;
	my $b = $sub_kmer =~ tr/1/1/;
	my $c = $sub_kmer =~ tr/2/2/;
	my $e = $sub_kmer =~ tr/3/3/;
	my $f = $sub_kmer =~ tr/4/4/;
	my $g = $sub_kmer =~ tr/5/5/;
	my $h = $sub_kmer =~ tr/6/6/;
	my $i = $sub_kmer =~ tr/7/7/;
	my $j = $sub_kmer =~ tr/8/8/;
	my $k = $sub_kmer =~ tr/9/9/;
	my $l = $sub_kmer =~ tr/M/M/;
	print OUT $_,"\t",$GC_ratio,"\t",$repeat_ratio,"\t",$gap_ratio,"\t",$a,"\t",$b,"\t",$c,"\t",$e,"\t",$f,"\t",$g,"\t",$h,"\t",$i,"\t",$j,"\t",$k,"\t",$l,"\n";
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

