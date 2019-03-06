#!/usr/bin/perl
use strict;
use Data::Dumper;
=pod
#################family id#################
trio_1_114989   trio_1_05537    trio_1_1500475
trio_2_09331    trio_2_1202016  trio_2_1500451
trio_3_11009    trio_2_1202016  trio_3_1100850
###########################################
=cut
die "Usage: perl $0 <family ID{one trio per line}> <GenomeStrip table> <trio number> <out>\n" unless @ARGV == 4;
open (IN1, "$ARGV[0]") or die "family ID missing\n";
open (IN2, "$ARGV[1]") or die "GenomeStrip table file required!\n";
open (OUT, ">$ARGV[3]") or die "permission denied!\n";
my @trio;
while(<IN1>){
	chomp;
	push @trio, (split/\s+/,$_);
}
close IN1;
print STDERR "@trio\n";
my @trio_index;
while(<IN2>){
	chomp;
	if (/^chr/){
		my @header = split/\t/;
		my %hash;
		my $tmp = -1;
		foreach my $tmp_head (@header){
			$tmp++;
			next if exists $hash{$tmp_head};
			$hash{$tmp_head} = $tmp;
		}
		foreach my $trio_individual (@trio){
			die "id error $trio_individual\n" unless exists $hash{$trio_individual};
			push @trio_index, $hash{$trio_individual};
		}
		print STDERR "Trio index:",join ("_", @trio_index),"\n";
		print OUT $_,"\t","error\n";
	}
	else{
		my @genotype = split/\t/;
		if ($genotype[4] eq "PASS" and $_ !~ /LQ/){
			my @trio_genotype = @genotype[@trio_index];
			my @allele;
			foreach my $tmp (@trio_genotype){
				push @allele, (split/\//,(split/:/,$tmp)[0]);
			}
			my $right = 0;
			foreach my $trio_number (1..$ARGV[2]){
				my %possible;
				my $par1 = shift @allele;
				my $par2 = shift @allele;
				my $par3 = shift @allele;
				my $par4 = shift @allele;
				my $childern1 = shift @allele;
				my $childern2 = shift @allele;
				$possible{$par1.$par3} = 1;
				$possible{$par1.$par4} = 1;
				$possible{$par2.$par3} = 1;
				$possible{$par2.$par4} = 1;
				$possible{$par3.$par1} = 1;
				$possible{$par4.$par1} = 1;
				$possible{$par3.$par2} = 1;
				$possible{$par4.$par2} = 1;
				if (exists $possible{$childern1.$childern2}){
					$right++;
				}
			}
			print OUT  $_,"\t",$ARGV[2]-$right,"\n";
		}
		else{
			print OUT  $_,"\t","NA","\n";
		}
	}
}
close IN2;
close OUT;
