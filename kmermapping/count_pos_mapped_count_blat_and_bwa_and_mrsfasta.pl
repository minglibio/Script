#!/usr/bin/perl
use strict;
my $command = $ARGV[0];
die "command must be bam, psl or mrsfasta\n" unless ($command eq "bam" or $command eq "psl" or $command eq "mrsfasta");
if ($command eq "bam"){
	die "Usage: perl $0 $command <bam [same oder with kmer]> <step_size> <output>\n" unless @ARGV == 4;
	open (IN, "-|", "samtools view -F 0x500 $ARGV[1]") or die "$!\n"; #remove PCR or optical duplicate and secondary mapped
	open (OUT, ">$ARGV[3]") or die "permission denied!\n";
	my $multi_count;
	my $step_size = $ARGV[2];
	my %hash;
	while (<IN>){
		chomp;
		my @tmp = split/\s+/;
		my @read = split/_/, $tmp[0];
		pop @read;
		my $read_id = join("_", @read);
		if ($_=~/\sXA:Z:(.+;)/) {
        		$multi_count =()=$1=~/;/g;
			if ($multi_count < 9){
				foreach (1..$step_size){
					push @{$hash{$read_id}}, $multi_count+1;
				}
			}else{
				foreach (1..$step_size){
					push @{$hash{$read_id}}, "M";
				}
			}
        	}
		elsif ($tmp[2] eq "*"){
			foreach (1..$step_size){
				push @{$hash{$read_id}}, 0;
			}
		}
		else{
			foreach (1..$step_size){
				push @{$hash{$read_id}}, 1;
			}
		}
	}
	close IN;
	foreach my $chr (keys %hash){
		print OUT ">$chr","\n";
		my $seq = join ("", @{$hash{$chr}});
		if (length($seq) > 100){
			my @tmp_seq = $seq =~ /\w{100}/g;
			if (length($') > 0){
				print OUT join "\n",(@tmp_seq, $', "");
			}else{
				print OUT join "\n",(@tmp_seq, "");
			}
		}else{
			print OUT $seq,"\n";
		}
	}
	close OUT;
}
elsif ($command eq "mrsfasta"){
	die "Usage: perl $0 $command <SAM> <kmer fasta> <step size> <output>\n" unless @ARGV == 5;
	my $stepsize = $ARGV[3];
	open (INSAM, "$ARGV[1]") or die "SAM file required!\n";
	open (INfasta, "$ARGV[2]") or die "fasta file required!\n";
	open (OUTmrsfasta, ">$ARGV[4]") or die "permission denied!\n";
	my %count;
	while (<INSAM>){
		chomp;
		next if (/^\@/);
		my @v = split /\s+/;
		next if $v[2] eq "*";
		$count{$v[0]}++;
	}
	print STDERR "SAM file loading finished!\n";
	close INSAM;
	my %result;
        my $multi_count;
	my $nohit_num = 0;
        while (<INfasta>){
                next unless /^>/;
                s/>//;
                chomp;
                if (exists $count{$_}){
                        $multi_count = $count{$_};
                }
                else {	
			$nohit_num++;
                        $multi_count = 0;
                }
                my @read = split/_/, $_;
		pop @read;
		my $chr = join("_", @read);
		for (my $i = 1; $i <= $stepsize; $i += 1){
                        if ($multi_count > 9){
                                push @{$result{$chr}}, "M";
                        }
                        else {
                                push @{$result{$chr}}, $multi_count;
                        }
                }
        }
        close INfasta;
	print STDERR "no hit number: $nohit_num\n";
	foreach my $chr (keys %result){
		print OUTmrsfasta ">$chr","\n";
		my $seq = join ("", @{$result{$chr}});
		if (length($seq) > 100){
			my @tmp_seq = $seq =~ /\w{100}/g;
			if (length($') > 0){
				print OUTmrsfasta join "\n",(@tmp_seq, $', "");
			}else{
				print OUTmrsfasta join "\n",(@tmp_seq, "");
			}
		}else{
			print OUTmrsfasta $seq,"\n";
		}
	}
        close OUTmrsfasta;
}
elsif ($command eq "psl"){
	die "Usage: perl $0 $command <PSL> <kmer fasta> <step size> <output>\n" unless @ARGV == 5;
	my $stepsize = $ARGV[3];
	open (INpsl, "$ARGV[1]") or die "psl file required!\n";
	open (INfasta, "$ARGV[2]") or die "fasta file required!\n";
	open (OUTpsl, ">$ARGV[4]") or die "permission denied!\n";
	my %count;
	while (<INpsl>){
		chomp;
		next unless (/^\d/);
		my @v = split /\s+/;
		next if $v[7] >= 5;
		if(@v == 22) {shift(@v);} # ucsc psl starts with a 'bin' field?
		next unless (@v == 21); #die "# error: doesnt look like psl format I know"
		$count{$v[9]}++;
	}
	close INpsl;
	my %result;
	my $multi_count;
	while (<INfasta>){
		next unless /^>/;
		s/>//;
		chomp;
		if (exists $count{$_}){
			$multi_count = $count{$_};
		}
		else {
			$multi_count = 0;
		}
		my @read = split/_/, $_;
		pop @read;
		my $chr = join("_", @read);
		for (my $i = 1; $i <= $stepsize; $i += 1){
			if ($multi_count > 9){
				push @{$result{$chr}}, "M";
			}
			else {
				push @{$result{$chr}}, $multi_count;
			}
		}
	}
	close INfasta;
	foreach my $chr (keys %result){
		print OUTpsl ">$chr","\n";
		my $seq = join ("", @{$result{$chr}});
		if (length($seq) > 100){
                	my @tmp_seq = $seq =~ /\w{100}/g;
			if (length($') > 0){
				print OUTpsl join "\n",(@tmp_seq, $', "");
			}else{
				print OUTpsl join "\n",(@tmp_seq, "");
			}
		}else{
			print OUTpsl $seq,"\n";
		}
	}
	close OUTpsl;
}
