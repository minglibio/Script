#!/usr/bin/perl -w
use strict;
die "command must be vcftable, select, statis, refine, poolfrq, missingrate, vcf_to_fasta\n" unless defined $ARGV[0];
my $command = $ARGV[0];
die "command must to vcftable, select, statis, refine, poolfrq, missingrate, vcf_to_fasta\n" unless ($command eq "vcftable" or $command eq "select" or $command eq "statis" or $command eq "refine" or $command eq "poolfrq" or $command eq "missingrate" or $command eq "vcf_to_fasta"); 
if ($command eq "vcftable"){
	die "Usage:perl $0 <vcf|gzip vcf> <haploid/diploid> <min depth> <out>\nOUT format:\nchr pos ref alt depthsum genotype depth\n" unless @ARGV == 5;
	my $input = $ARGV[1];
	open (IN,($input =~ /\.gz$/)? "gzip -dc $input |" : $input) or die "gzipped vcf file required!\n";
	open (OUT, ">$ARGV[4]") or die "permission denied!\n";
	while(<IN>){
		next if /^##/;
		chomp;
		if (/^#CHROM/){
			my @header = split/\t/;
			print OUT "$header[0]\t$header[1]\t$header[3]\t$header[4]\tDepth\t";
			my @sample = @header[9..$#header];
			print OUT join("\t", @sample),"\n"; #"\t",join("\t", @sample),"\n";
		}
		else{
			my @tmp = split/\t/;
			my $dpsum = 0;
			my @genotype;
			my @depth;
			print OUT "$tmp[0]\t$tmp[1]\t$tmp[3]\t$tmp[4]\t";
			if ($ARGV[2] eq 'haploid'){	
				foreach my $index (9..$#tmp){
					my @inf = split/:/, $tmp[$index];
					if (defined $inf[1]){
						$dpsum += $inf[1];
						my $tmpgenotype = $inf[1] >= $ARGV[3] ? $inf[0] : ".";
						push @genotype, $tmpgenotype;
						push @depth, $inf[1];
					}
					else{
						my $tmpgenotype = ".";
						push @genotype, $tmpgenotype;
						push @depth, 0;
					}
				}
				print OUT $dpsum,"\t",join("\t",@genotype),"\t",join("\t",@depth),"\n";
			}
			elsif($ARGV[2] eq 'diploid'){
				foreach my $index (9..$#tmp){
					my @inf = split/:/, $tmp[$index];
					if (defined $inf[1]){
						my ($refdp,$altdp) = split/,/,$inf[1];
						#my $dp = $refdp+$altdp;
						my $dp = $inf[2];
						$dpsum += $dp;
						my $tmpgenotype = $dp >= $ARGV[3] ? $inf[0] : ".";
						$tmpgenotype =~ s/\//|/g;
						push @genotype, $tmpgenotype;
						push @depth, $inf[1];
					}
					else{
						my $tmpgenotype = ".";
						push @genotype, $tmpgenotype;
						push @depth, 0;
					}
				}
				print OUT $dpsum,"\t",join("\t",@genotype),"\n"; #"\t",join("\t",@depth),"\n";
			}
		}
	}
	close IN;
	close OUT;
}
elsif($command eq "select"){
	die "Usage:perl $0 <list> <table> <out>\nselecte some samples from vcftable results\n" unless @ARGV == 4;
	open (IN1, "$ARGV[1]") or die "select list required!\n";
	open (IN2, "$ARGV[2]") or die "table required!\n";
	open (OUT, ">$ARGV[3]") or die "permission denied\n";
	my %selected;
	while(<IN1>){
		chomp;
		my @tmp = split/\t/;
		$selected{$tmp[0]} = 1;
	}
	close IN1;
	my $header = <IN2>; chomp $header; my @tmp_header = split/\t/, $header;
	my $index = -1;
	my @select = (0..4);
	foreach my $sample (@tmp_header){
		$index++;
		push @select, $index if exists $selected{$sample};
	}
	my @selected_head = @tmp_header[@select];
	print STDERR join("\t", @select),"\n";
	print OUT join("\t", @selected_head),"\n";
	while(<IN2>){
		chomp;
		my @tmp_inf = split/\t/;
		my @select_inf = @tmp_inf[@select];
		print OUT join ("\t", @select_inf),"\n";
	}
	close IN2;
	close OUT;
}
elsif($command eq "statis"){
	die "Usage:perl $0 <vcf|gzip vcf> <out>\n(haploid)OUT FORMAT:\nchr pos ref alt INFO_DP sum_dp ref_count alt_count third_count\n" unless @ARGV == 3;
	my $input = $ARGV[1];
	open (IN,($input =~ /\.gz$/)? "gzip -dc $input |" : $input) or die "gzipped vcf file required!\n";
	open (OUT, ">$ARGV[2]") or die "permission denied!\n";
	while(<IN>){
		next if /^#/;
		chomp;
		my @tmp = split/\t/;
		my ($DP) = $tmp[7] =~ /DP=(\d+);/;
		my $sample_dp = 0;
		my $ref = 0;
		my $alt = 0;
		my $thirdallele = 0;
		foreach my $index(9..$#tmp){
			my $sample_tmp_dp = (split/:/,$tmp[$index])[1];
			my $sample_tmp_ref = (split/:/,$tmp[$index])[0];
			$sample_dp += $sample_tmp_dp;
			if ($sample_tmp_dp >= 1){
				if ($sample_tmp_ref == 0){
					$ref++;
				}
				elsif($sample_tmp_ref == 1){
					$alt++;
				}
				else{
					$thirdallele++;
				}
			}			
		}
		print OUT "$tmp[0]\t$tmp[1]\t$tmp[3]\t$tmp[4]\t$DP\t$sample_dp\t$ref\t$alt\t$thirdallele\n";
	}
	close IN;
	close OUT;
}
elsif($command eq "refine"){	
	die "Usage:perl $0 <vcf|gzip vcf> <min depth> <max missing> <out>\n" unless @ARGV == 5;
	my $input = $ARGV[1];
	open (IN,($input =~ /\.gz$/)? "gzip -dc $input |" : $input) or die "gzipped vcf file required!\n";
	open (OUT, ">$ARGV[4]") or die "permission denied!\n";
	while(<IN>){
		if (/^#/){
			print OUT $_;
		}
		else{
			chomp;
			my @tmp = split/\t/;
			my @genotype;
			my $miss_ind = 0;
			foreach my $index(9..$#tmp){
				my $sample_dp = (split/:/,$tmp[$index])[1];
				if ($sample_dp <= $ARGV[2]){
					$miss_ind++;
					push @genotype, ".";
				}
				else{
					push @genotype, $tmp[$index];
				}
			}
			if ($miss_ind <= $ARGV[3]){
				print OUT join("\t", @tmp[0..8]),"\t",join("\t", @genotype),"\n";
			}
		}
	}
	close IN;
	close OUT;
}
elsif($command eq "poolfrq"){
	die "Usage:perl $0 <vcf|gzip vcf> <pop list> <out>\n(diploid)pooling frequency for phyhip\n" unless @ARGV == 4;
	my $input = $ARGV[1];
	open (IN,($input =~ /\.gz$/)? "gzip -dc $input |" : $input) or die "gzipped vcf file required!\n";
	open (LIST, "$ARGV[2]") or die "population list required!\n";
	open (OUT, ">$ARGV[3]") or die "permission denied!\n";
	my %poplation;
	while(<LIST>){
		chomp;
		my @tmp_pop = split/\s+/;
		die "error: population name shouldn't more than 10 bytes\n" unless length($tmp_pop[1]) <= 10;
		$poplation{$tmp_pop[1]}{$tmp_pop[0]} = 1;
	}
	close LIST;
	my %pop_index;
	my %fre;
	my $effective_site = 0;
	my $pop_num = 0;
	while(<IN>){
		next if /^##/;
		chomp;
		if (/^#CHROM/){
			my @header = split/\t/;
			foreach my $pop (keys %poplation){
				$pop_num++;
				my $tmp_number = 0;
				foreach my $index(9..$#header){
					if (exists $poplation{$pop}{$header[$index]}){
						$tmp_number++;
						push @{$pop_index{$pop}}, $index;
					}
				}
				print STDERR $pop,"\t",$tmp_number,"\t",join("-", @{$pop_index{$pop}}),"\n";
			}
			print STDERR "Popnum:$pop_num\n";
		}
		else{
			my @tmp = split/\t/;
			my $effective_pop = 0;
			foreach my $pop (keys %pop_index){
				my $refdp = 0;
				my $altdp = 0;
				my $ref_sum = 0;
				my $alt_sum = 0;
				foreach my $ind_index (@{$pop_index{$pop}}){
					next unless ($tmp[$ind_index] =~ /^0\/0|^0\|0|^0\/1|^0\|1|^1\|0|^1\/1|^1\|1/);
					my @inf = split/:/, $tmp[$ind_index];
					($refdp,$altdp) = split/,/,$inf[1];
					$ref_sum += $refdp;
					$alt_sum += $altdp;
				}
				last unless $ref_sum+$alt_sum > 0;
				$effective_pop++;
			}
			if ($effective_pop == $pop_num){
				$effective_site++;
				foreach my $pop (keys %pop_index){
					my $refdp = 0; my $altdp = 0;my $ref_sum = 0;my $alt_sum = 0;
					foreach my $ind_index (@{$pop_index{$pop}}){
						next unless ($tmp[$ind_index] =~ /^0\/0|^0\|0|^0\/1|^0\|1|^1\|0|^1\/1|^1\|1/);
						my @inf = split/:/, $tmp[$ind_index];
						($refdp,$altdp) = split/,/,$inf[1];
						$ref_sum += $refdp;
						$alt_sum += $altdp;
						my $ref_fre = sprintf "%.3f",$ref_sum/($ref_sum+$alt_sum);
						push @{$fre{$pop}}, $ref_fre;
					}
				
				}
				
			}
		}
	}
	print STDERR "effective site:$effective_site\n";
	close IN;
	my @allel_number;
	push (@allel_number, 2) for(1..$effective_site);
	print OUT "$pop_num  $effective_site\n",join(" ", @allel_number),"\n";
	foreach my $pop (keys %fre){
		my @blank;
		push @blank, " " foreach (1..(10-length($pop)));
		print OUT $pop, join("",@blank)," ";
		print OUT join(" ",@{$fre{$pop}}),"\n";
	}
	close OUT;
}
elsif($command eq "missingrate"){
	die "Usage:perl $0 <vcf|gzip vcf> <min depth> <out>\n(haploid) OUT FORMAT\nsample miss miss_rate effective_site\n" unless @ARGV == 4;
	my $input = $ARGV[1];
	open (IN,($input =~ /\.gz$/)? "gzip -dc $input |" : $input) or die "gzipped vcf file required!\n";
	open (OUT, ">$ARGV[3]") or die "permission denied!\n";
	my @sample;
	my $total = 0;
	my %miss;
	while(<IN>){
		next if /^##/;
		chomp;
		if (/^#CHR/){
			@sample = split/\t/;
		}		
		else{
			my @geno = split/\t/;
			$total++;
			foreach my $index (9..$#geno){
				my $sample_dp = (split/:/,$geno[$index])[1];
				if ($sample_dp < $ARGV[2]){
					$miss{$sample[$index]}++;
				}
			}
		}
	}
	foreach my $sample (sort keys %miss){
		my $miss_rate = $total > 0 ? sprintf "%.3f",$miss{$sample}/$total : 0;
		print OUT $sample,"\t",$miss{$sample},"\t",$miss_rate,"\t",$total,"\n";
	}
}
elsif($command eq "vcf_to_fasta"){
=pod
mafft --thread 10 --phylipout --reorder --auto 03.fa >sheepY.phy
=cut
	die "Usage : perl $0 <vcf|vcf.gz> <haploid/diploid> <output>\n" unless @ARGV == 4;
	my $input = $ARGV[1];
	open (IN,($input =~ /\.gz$/)? "gzip -dc $input |" : $input) or die "gzipped vcf file required!\n";
	open (OUT, ">$ARGV[3]") or die "permission denied!\n";
	my %seq;
	my $site = 0;
	my %sequence;
	while (<IN>){
		next if /^##/;
		chomp;
		if (/^#CHR/){
			my @head = split/\t/;
			foreach (9..$#head){
				$seq{$_} = $head[$_];
			}
		}
		else{
			if ($ARGV[2] eq 'haploid'){
				my @genotype = split/\t/;
				my $ref = $genotype[3];
				my $alt = $genotype[4];
				next unless (length($alt) == 1 and length($ref) == 1);
				$site++;
				foreach (9..$#genotype){
					if ($genotype[$_] =~ /^0/){
						push @{$sequence{$seq{$_}}}, $ref;
					}
					elsif($genotype[$_] =~ /^1/){
						push @{$sequence{$seq{$_}}}, $alt;
					}
					elsif($genotype[$_] =~ /^\./){
						push @{$sequence{$seq{$_}}}, 'N';
					}
					else{
						print STDERR "contain multiple allele sites!\n";
					}
				}
			}
			elsif ($ARGV[2] eq 'diploid'){
				my %degenerate = (
					'AG' => 'R',
					'CT' => 'Y',
					'AC' => 'M',
					'GT' => 'K',
					'GC' => 'S',
					'AT' => 'W',
				);
				my @genotype = split/\t/;
				my $ref = $genotype[3];
				my $alt = $genotype[4];
				next unless (length($alt) == 1 and length($ref) == 1);
				my $degenerate_genotype = defined $degenerate{$ref.$alt} ? $degenerate{$ref.$alt} : $degenerate{$alt.$ref};
				$site++;
				foreach (9..$#genotype){
					if ($genotype[$_] =~ /^0\/0/ or $genotype[$_] =~ /^0\|0/){
						push @{$sequence{$seq{$_}}}, $ref;
					}
					elsif($genotype[$_] =~ /^0\/1/ or $genotype[$_] =~ /^1\/0/ or $genotype[$_] =~ /^0\|1/ or $genotype[$_] =~ /^1\|0/){
						push @{$sequence{$seq{$_}}}, $degenerate_genotype;
					}
					elsif($genotype[$_] =~ /^1\/1/ or $genotype[$_] =~ /^1\|1/){
						push @{$sequence{$seq{$_}}}, $alt;
					}
					elsif($genotype[$_] =~ /^\.\/\./ or $genotype[$_] =~ /^\.\|\./ or $genotype[$_] =~ /^\./){
						push @{$sequence{$seq{$_}}}, 'N';
					}
					else{
						print STDERR "$genotype[0]\t$genotype[1] $ref\t$alt $genotype[$_] contain non-bia sites\n";
					}
				}
			}
		}
	}
	print STDERR $site,"\n";
	close IN;
	foreach my $header (keys %sequence){
		print OUT ">$header\n",join("",@{$sequence{$header}}),"\n";
	}
	close OUT;
}
