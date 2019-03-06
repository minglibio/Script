#!/usr/bin/perl
use strict;
die "Usage : perl $0 <kmer count fasta> <db region> <output>\n" unless @ARGV == 3;
=pod
0 based region
chr	start	end	..
=cut
my $storefile = &FastaReader($ARGV[0]) or die "fasta file is required!\n";
open (IN,"$ARGV[1]") or die "region file required\n";
open (OUT,">$ARGV[2]") or die "permission denied\n";
while(<IN>){
	chomp;
	my @array=split /\s+/;
	my $chr = $array[0];
	my $start = $array[1];
	my $end = $array[2];
	my $sequence = substr($storefile->{$chr}, $start, $end-$start);
	print STDERR "$_\n" if ($sequence =~ /0/);
	next unless $sequence =~ /7|8|9|M/;
	print OUT "$array[0]\t$array[3]\n";
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
		my $tmp = (split/\s+/,$head)[0];
		$seq =~ s/\s+//g;
		$hash{$tmp} = $seq;
        }
	close IN;
	$/ = "\n";
	return \%hash;
}
