#!/usr/bin/perl
use strict;
die "Usage: perl $0 <blat kmer> <bwa kmer> <mrsfast kmer> <output>\n" unless @ARGV == 4;
my $blatkmer = &FastaReader($ARGV[0]) or die "blat kmer fasta file is required!\n";
my $bwakmer = &FastaReader($ARGV[1]) or die "bwa kmer fasta file is required!\n";
my $mrsfastkmer = &FastaReader($ARGV[2]) or die "mrsfast kmer fasta file is required!\n";
print STDERR "kmer fasta loading finished!\n";
open (OUT, ">$ARGV[3]") or die "permission denied!\n";
foreach my $head (sort {$a <=> $b} keys %{$blatkmer}){
	foreach my $window (1..(int(length($blatkmer->{$head})/50)-1)){
		my $blat_seq = substr ($blatkmer->{$head},($window-1)*50, 50);
		my $bwa_seq = substr ($bwakmer->{$head},($window-1)*50, 50);
		my $mrsfast_seq = substr ($mrsfastkmer->{$head},($window-1)*50, 50);
		my $blat_count = (split//, $blat_seq)[0];
		my $bwa_count = (split//, $bwa_seq)[0];
		my $mrsfast_count =(split//, $mrsfast_seq)[0];
		print OUT $head,"\t",($window-1)*50,"\t",$blat_count,"\t",$bwa_count,"\t",$mrsfast_count,"\n";
	}
}
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
