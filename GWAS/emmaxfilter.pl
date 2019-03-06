#!/usr/bin/perl -w 
use warnings;
use strict;
# Declare and initialize variables 
my @file1_data1 = (  ); 
my $file1_data1;
my @file1_data2 = (  ); 
my $file1_data2;

die  "Version 1.0\t2013-08-29;\nUsage: $0 <InPut1:only-for-PLINK-cov-output><OutDir:assoc>\n" unless (@ARGV ==2);

open     INFile,"$ARGV[0]"  || die "input file can't open $!" ;
open     OutFile,">$ARGV[1]" || die "output file can't open $!" ;

@file1_data1 = <INFile>; 
my $query1 = @file1_data1;
my $i = 0;

close  INFile;
print OutFile "CHR\tBP\tP\n"; 
    for ($i=1; $i<$query1; $i++)   # The number of whole raw snp number;
    {
        my @temp1 = split (/\s+/, $file1_data1[$i]);
        my $temp1_len = @temp1 ;
#        $temp1[0] =~ s/32/29/;
        if ($temp1[0] > 0 && $temp1[3] > 0 )
        {
        print OutFile "$temp1[0]\t$temp1[2]\t$temp1[3]\n";
        }
    }
close (OutFile) or die( "Cannot close file : $!");
