#!/usr/bin/perl
use strict;
die "Usage : perl $0 <ref fasta> <region> <output>\n" unless @ARGV == 3;
=pod
#ref fasta
>1 dna_sm:chromosome chromosome:Galgal4:1:1:195276750:1 REF
catgacacttttgaacaatttcatggggtggtttggacggggaaaggctagccccataag
tgaagttttgccagggcacatcccgggattcctaggatccccatatcatgggattgcttg
>Z dna_sm:chromosome chromosome:Galgal4:Z:1:82363669:1 REF
ttttaacctttcgggacccatccaaccacaaccaccccatacatataggacctgtaagac
cccttccaacccaacccaaccatcctatacctctttccccttccaggacccacccacccc
=cut
=pod
####region######
chr     start   end
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
        my $sequence = substr($storefile->{$chr}, $start-1, $end-$start+1);
        print OUT ">$chr","_","$start","_","$end\n$sequence\n";
}
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
