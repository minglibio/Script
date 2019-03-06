#!/usr/bin/perl

#########################################################################
## Author: Hechuan Yang
## Created Time: 2014-10-08 16:48:59
## File Name: sliding_w.pl
## Description: 
##########################################################################
use strict;
use warnings;
use Getopt::Std;

my %opts;

getopts('c:p:d:w:s:Sh',\%opts);

die("
Description:
    Get the mean/sum of depth through genome by sliding window.
Useage: 
    $0  [-c INT -p INT -w INT -s INT -S -h] <INPUT>
Options:
    -c INT the column of chromosome name[1]
    -p INT the column of position[2]
    -d INT the column of depth[8]
    -w INT the window size[100000]
    -s INT the step size[20000]
    -S     print the SUM of depth over every sites in windows, Not mean depth
    -h     print this message

") if $opts{h} || @ARGV==0;


my $chr=$opts{c}?$opts{c}-1:0;
my $pos=$opts{p}?$opts{p}-1:1;
my $depth=$opts{d}?$opts{d}-1:7;
my $window_size=$opts{w}?$opts{w}:100000;
my $step_size=$opts{s}?$opts{s}:20000;
my (@window,$start,$end,$mean_depth);

while(@window==0)
{
	my @line=split/\s+/,<>;    #filter can be added right after this line (1/2)
	($start,$end)=&chr_head($line[$chr],1,$line[$pos]);
	push @window,\@line;
}

while(<>)
{
	my @line=split;            #filter can be added right after this line (2/2)      
	if($line[$chr] ne ${$window[-1]}[$chr] )  #the first line of a new chromosome
	{
		$mean_depth=&coverage(\@window);
		&output(${$window[-1]}[$chr],$start+$window_size/2,$mean_depth);
		@window=();
		($start,$end)=&chr_head($line[$chr],1,$line[$pos]);
	}
	elsif($line[$pos] > $end)  #outside the window
	{
		do
		{
			if(@window)
			{
				$mean_depth=&coverage(\@window);
				&output(${$window[-1]}[$chr],$start+$window_size/2,$mean_depth);
				my $next_start=$start+$step_size;
				while(@window && ${$window[0]}[$pos]<$next_start)
				{
					shift @window;
				}
			}
			else
			{	
				&no_cover_output($line[$chr],$start+$window_size/2);
			}
			$start+=$step_size;
                        $end+=$step_size;
		}while($line[$pos]>$end)
	}
        push @window,\@line;
}
$mean_depth=&coverage(\@window);
&output(${$window[-1]}[$chr],$start+$window_size/2,$mean_depth);

sub coverage
{
	my $window_full=shift;
	my $depth_sum;
	for(@$window_full)
	{
		$depth_sum+=$$_[$depth];
	}
	if(@$window_full<$window_size)
	{
		for(@$window_full..$window_size-1)
		{
			$depth_sum+=0;
		}
	}
    if($opts{S}){
        return $depth_sum;
    }
    else{
        return $depth_sum/$window_size;
    }
}

sub output
{
	print join("\t",@_),"\n";
}

sub no_cover_output
{
	print join("\t",@_,0),"\n";         #output when no reads locate in this window
}

sub chr_head
{
	my $chr=shift;
	my $start=shift;
	my $out=shift;
	my $end=$start+$window_size-1;
	for(;$end<$out;$end+=$step_size)
        {
                &no_cover_output($chr,$end-$window_size+1);
        }
	return ($end-$window_size+1,$end)
}

