#! /usr/bin/perl -w
use strict;
die "Usage: perl get_taxonomy_info.pl <blast_m8_list> <gi_taxid> <name_dmp> <node_dmp> <outfile>\n" unless @ARGV == 5;
open (BLAST,"$ARGV[0]") or die "Blast best result required!\n";
my %gihash;
while(<BLAST>){
	chomp;
	my @inf= split /\t/;
	$inf[1]=~ /gi\|(\d+)\|.+\|*(.+)\|/;
	my $gi=$1; 
	my $id= $2;
	$gihash{$gi}=$id;
}
my $gi_tax = $ARGV[1];
open (GT,($gi_tax =~ /\.gz$/)? "gzip -dc $gi_tax |" : $gi_tax) or die "gi_taxid_nucl.dmp file required!\n";
my %gi_tax_hash;
while(<GT>){
	chomp;
	my @tmp = split /\t/;
	if(exists $gihash{$tmp[0]}){
		$gi_tax_hash{$tmp[0]}= $tmp[1];
	}
}
close GT;
print STDERR "gi_taxid_nucl.dmp file loading finished!\n";
open (TN, "$ARGV[2]") or die "names.dmp file required!\n";
my %tax_name_hash;
while(<TN>){
	chomp;
	my @inf = split /\t\|\t/;
	$inf[3]=~ s/\t\|//g;
	if($inf[3] eq "scientific name"){
		$tax_name_hash{$inf[0]} = $inf[1];
	}
}
close TN;
open (NOD,"$ARGV[3]") or die "nodes.dmp file required!\n";
my %parent_hash;
my %rank_hash;
while(<NOD>){
	chomp;
	my @inf = split /\t\|\t/;
	$parent_hash{$inf[0]} = $inf[1];
	$rank_hash{$inf[0]} = $inf[2];
}
close NOD;

seek BLAST, 0, 0;
open (OUT, ">$ARGV[4]") or die "permission denied!\n";
while(<BLAST>){
	chomp;
	my @inf = split /\t/;
	$inf[1] =~ /gi\|(\d+)\|.+\|*(.+)\|/;
	my $gi = $1;
	my $id = $2;
	my $tax = exists $gi_tax_hash{$gi} ? $gi_tax_hash{$gi} : 0;
	my $parent_tax = exists $parent_hash{$tax} ? $parent_hash{$tax} : 1;
	my @alltax = ("NA") x 7;
	$alltax[0] = $tax;
	while($parent_tax != 1){
		if($rank_hash{$parent_tax} eq "genus"){$alltax[1] = $parent_tax;}
		if($rank_hash{$parent_tax} eq "family"){$alltax[2] = $parent_tax;}
		if($rank_hash{$parent_tax} eq "order"){$alltax[3] = $parent_tax;}
		if($rank_hash{$parent_tax} eq "class"){$alltax[4] = $parent_tax;}
		if($rank_hash{$parent_tax} eq "phylum"){$alltax[5] = $parent_tax;}
		if($rank_hash{$parent_tax} eq "superkingdom"){$alltax[6] = $parent_tax;}
		$parent_tax = $parent_hash{$parent_tax}; #one and one up
	}
	print OUT "$_\t";
	foreach my $tmp (@alltax){
		if(!exists $tax_name_hash{$tmp}){
			$tax_name_hash{$tmp} = "NA";
		}
		print OUT "$tax_name_hash{$tmp}|";
	}
	print OUT "\n";
}
close BLAST;
close OUT;
open (SAT, "$ARGV[4]") or die "parse tax id incompleted\n";
my %class_stastic;
my $recode = 0;
while(<SAT>){
	chomp;
	my @inf = split/\t/;
	my @tmp = split /\|/,$inf[-1];
	if (defined $tmp[4]){
		$class_stastic{$tmp[4]}++;
		$recode++;
	}
	else{
		print STDERR "$_\n"
	}
}
close SAT;
foreach my $tmp_class (sort {$class_stastic{$a} <=> $class_stastic{$b}} keys %class_stastic){
	print STDERR $tmp_class,"\t",$class_stastic{$tmp_class},"\t",$class_stastic{$tmp_class}/$recode,"\n";
}
