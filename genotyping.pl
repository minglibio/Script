#!/usr/bin/perl
use strict;
use Data::Dumper;
die "Usage : perl $0 <database> <CNVR> <sample number>\n" unless @ARGV == 3;
open (IN1, "$ARGV[0]") or die "Table required!\n";
open (IN2, "$ARGV[1]") or die "Input CNVR file!\n";
my $sample_num = $ARGV[2];
my $i;
my $n_01;my $n_02;my $n_11;my $n_12;my $n_21;my $n_22;my $n_31;my $n_32;
my %database;my %database2;my %database3;my %database4;my %database5;my %database6;my %database7;my %database8;
my $m1; my $m2; my $a; my $b;
my $x01;my $x02;my $x11;my $x12;my $x21;my $x22;my $x31;my $x32;
my $pl;my $average;
my $select; my $rd;
my $genotyping_aa;my $genotyping_Aa;my $genotyping_AA; my $genotyping_AB; my $genotyping_BB;my $genotyping_BC;my $genotyping_M;
my @biaotou;my @zhongjian;
my $n1;my $n2;my $n3;

while(<IN1>){
	chomp;
	my @data = split/\s+/;

	$database{"$data[0]-$data[1]"} = $data[2];           #aaAaAA model,不平移，$data[0]是aa频率m1，$data[1]是Aa频率m2,$data[2]是阈值a,$data[3]是阈值b.
	$database2{"$data[0]-$data[1]"} = $data[3];          #<=a 属于aa; >a&&<=b 属于Aa; >b 属于AA
		  
	$database3{"$data[0]-$data[1]"} = $data[2]+1;        #AAABBB model,平移1，$data[0]是AA频率m1，$data[1]是AB频率m2,$data[2]是阈值a,$data[3]是阈值b.
	$database4{"$data[0]-$data[1]"} = $data[3]+1;        #<=a 属于AA; >a&&<=b 属于AB; >b 属于BB
		  
	$database5{"$data[0]-$data[1]"} = $data[2]+1.5;      #ABBBM model,平移1.5，$data[0]是AB频率m1，$data[1]是BB频率m2,$data[2]是阈值a,$data[3]是阈值b.
	$database6{"$data[0]-$data[1]"} = $data[3]+1.5;      #<=a 属于AB; >a&&<=b 属于BB; >b 属于M
		  
	$database7{"$data[0]-$data[1]"} = $data[2]+2;        #BBM model,平移2，$data[0]是BB频率m1，$data[1]是M频率m2,$data[2]是阈值a,$data[3]是阈值b.       
	$database8{"$data[0]-$data[1]"} = $data[3]+2;        #<=a 属于BB; >a&&<=b 属于M; >b 属于M(>a都属于M)
	
}
close IN1;

my $header = <IN2>;
chomp $header;
my @biaotou = split/\s+/, $header;
my @zhongjian = splice(@biaotou,8, $sample_num);
print $header,"\t",join("\t",@zhongjian),"\t","aa","\t","Aa","\t","AA","\t","AB","\t","BB","\t","BC","\t","M","\t","average1\taverage2\taverage3\tsd1\tsd2\tsd3","\n";
while(<IN2>){
	chomp;
	print $_;
	my @tmpkaishi = split/\s+/;
	my @average = splice(@tmpkaishi, $sample_num+8, 1);  ###整体的平均值
	my @tmp = splice(@tmpkaishi, 8, $sample_num); ##样本数
	if( $average[0]>=0 && $average[0]< 1.00 ){
		$pl = 0;                                           #平均值 >=0 && < 1.10 aaAaAA model
	}
	elsif( $average[0]>=1.00 && $average[0]< 2.00){
		$pl = 1.00;                                         #平均值 >=1.10 && < 2.10 AAABBB model
	}
	elsif( $average[0]>=2.00 && $average[0]< 2.5 ){
		$pl = 1.50;                                          #平均值 >=2.10 && < 2.75 ABBBM model
	}
	elsif($average[0]>= 2.5){
		$pl = 2;                                             #平均值 >=2.75 BMmodel
	}
	$n_01=$n_02=0;
	for $i(0..@tmp-1){
		if(@tmp[$i] <= 0.25+$pl){
			$n_01++;                                               #以0.25和0.75先卡，统计每一类型个数。
		} 
		elsif(@tmp[$i] > 0.25+$pl && @tmp[$i ]<= 0.75+$pl){
			$n_02++;
		}	
	}
	$x01= sprintf"%.2f",$n_01/@tmp;                            #算出初始频率。                 
	$x02= sprintf"%.2f",$n_02/@tmp;
	if ($x01+$x02>1){$x02 = sprintf"%.2f",(1-$x01)};
	if( $average[0]>=0 && $average[0]< 1.00 ){                  #往每一个模型里面代入，根据数据库频率得出阈值。
		$a=$database{"$x01-$x02"};                        
		$b=$database2{"$x01-$x02"};
	}
	elsif( $average[0]>=1.00 && $average[0]< 2.00){
		$a=$database3{"$x01-$x02"};                        
		$b=$database4{"$x01-$x02"};   
	}
	elsif( $average[0]>=2.00 && $average[0]< 2.5 ){
		$a=$database5{"$x01-$x02"};                        
		$b=$database6{"$x01-$x02"};
	}
	elsif($average[0]>= 2.5){
		$a=$database7{"$x01-$x02"};                        
		$b=$database8{"$x01-$x02"} ;
	}
	$n_11=$n_12=0;
	for $i(0..@tmp-1){
		if(@tmp[$i]<=$a){
			$n_11++;
		}
		elsif(@tmp[$i]>$a && @tmp[$i]<=$b){
			$n_12++;
		}
	}
	$x11= sprintf"%.2f",$n_11/@tmp;                      #第二次迭代结果
	$x12= sprintf"%.2f",$n_12/@tmp;
	if ($x11+$x12>1){$x02 = sprintf"%.2f",(1-$x11)};
	if( $average[0]>=0 && $average[0]< 1.00 ){
		$a=$database{"$x11-$x12"};
		$b=$database2{"$x11-$x12"};
	}
	elsif( $average[0]>=1.00 && $average[0]< 2.00){
		$a=$database3{"$x11-$x12"};
		$b=$database4{"$x11-$x12"};   
	}
	elsif( $average[0]>=2.00 && $average[0]< 2.5 ){
		$a=$database5{"$x11-$x12"};
		$b=$database6{"$x11-$x12"};
	}
	elsif($average[0]>= 2.5){
		$a=$database7{"$x11-$x12"};
		$b=$database8{"$x11-$x12"};
	}
	$n_21=$n_22=0;
	for $i(0..@tmp-1){
		if(@tmp[$i]<=$a){
			$n_21+=1;
		}
		elsif(@tmp[$i]>$a && @tmp[$i]<=$b){
			$n_22++;
		}
	}
	$x21= sprintf"%.2f",$n_21/@tmp;             #第三次迭代结果，如果闲迭代次数少，可以继续迭代，结果会收敛
	$x22= sprintf"%.2f",$n_22/@tmp;
	if ($x21+$x22>1){$x22 = sprintf"%.2f",(1-$x21)};
	if( $average[0]>=0 && $average[0]< 1.00 ){
		$a=$database{"$x21-$x22"};
		$b=$database2{"$x21-$x22"};
	}
	elsif( $average[0]>=1.00 && $average[0]< 2.00){
		$a=$database3{"$x21-$x22"};                        
		$b=$database4{"$x21-$x22"};
	}
	elsif( $average[0]>=2.00 && $average[0]< 2.5 ){
		$a=$database5{"$x21-$x22"};                        
		$b=$database6{"$x21-$x22"};
	}
	elsif( $average[0]>= 2.5){
		$a=$database7{"$x21-$x22"};
		$b=$database8{"$x21-$x22"};
	}
	$m1=$x21;
	$m2=$x22;
	$a=$a;
	$b=$b;
	print  "\t";
	
#################################################################################################################genotyping
	my @select = @tmp;
	my (@mode1, @mode2, @mode3);
	$genotyping_aa=$genotyping_Aa=$genotyping_AA=$genotyping_AB=$genotyping_BB=$genotyping_BC=$genotyping_M=0;
	foreach my $rd (@select){
		if ($a < 0.45 && $a > 0.1  and $b > 0.49 && $b < 0.96 ){             #阈值a、b绝对会在某个区间变动，看看数据库就知道了。
			if ($rd <= $a){
				print "dd\t";
				$genotyping_aa++;
				push @mode1, $rd;
			}
			elsif( $rd > $a and $rd <= $b){
				print "Ad\t";
				$genotyping_Aa++;
				push @mode2, $rd;
			}
			elsif($rd > $b){
				print "AA\t";
				$genotyping_AA++;
				push @mode3, $rd;
			}
		}
		elsif ($a < 1.45 && $a > 1.1 and $b > 1.49 && $b < 1.96){            
			if($rd <= $a){
				print "AA\t";
				$genotyping_AA++;
				push @mode1, $rd;
			}				   
			elsif($rd >$a and $rd <= $b){
				print "AB\t";
				$genotyping_AB++;
				push @mode2, $rd;
			}
			elsif($rd > $b){
				print "BB\t";
				$genotyping_BB++;
				push @mode3, $rd;
			}
		}
		elsif ($a < 1.95 && $a > 1.6 and $b > 1.99 && $b <2.46 ){
			if($rd <= $a){
				print "AB\t";
				$genotyping_AB++;
				push @mode1, $rd;
			}
			elsif($rd >$a and $rd <= $b){
				print "BB\t";
				$genotyping_BB++;
				push @mode2, $rd;
			}
			elsif($rd > $b){
				print "BC\t";
				$genotyping_BC++;
				push @mode3, $rd;
			}
		}
		elsif ( $a < 2.45 && $a > 2.1 and $b < 2.99){
			if($rd <= $a){
				print "BB\t";
				$genotyping_BB++;
				push @mode1, $rd;
			}
			elsif($rd > $a and $rd <= $b){
				print "BC\t";
				$genotyping_BC++;
				push @mode2, $rd;
			}elsif($rd >$b ){
				print "M\t";
				$genotyping_M++;
				push @mode3, $rd;
			}
		}
	}
	my $averagemode1 = &get_average(@mode1);my $sdmode1 = &get_sd(@mode1);
	my $averagemode2 = &get_average(@mode2);my $sdmode2 = &get_sd(@mode2); 
	my $averagemode3 = &get_average(@mode3);my $sdmode3 = &get_sd(@mode3);
	print "$genotyping_aa\t$genotyping_Aa\t$genotyping_AA\t$genotyping_AB\t$genotyping_BB\t$genotyping_BC\t$genotyping_M\t$averagemode1\t$averagemode2\t$averagemode3\t$sdmode1\t$sdmode2\t$sdmode3\n"; 
}
close IN2;
sub get_average {
	my @array = @_;
	my $sum;
	for my $value (@array) {
		$sum += $value;
	}
	my $average = @array > 0 ? sprintf "%.2f",$sum/@array : "NA";
	return $average;
}
sub get_sd {
	my @array = @_;
	my $sum;
	for my $value (@array) {
		$sum += $value;
	}
 	my $average = @array > 0 ? $sum/@array : 0;
 	$sum = 0;
 	for my $value (@array) {
		$sum += ($value-$average)**2;
	}
	my $sd = @array > 1 ? sprintf "%.2f",sqrt($sum/(@array-1)) : "NA";
	return $sd;
}
=pod			 
	##	F值	 
	$n1=$n2=$n3=0;
	my $sum_x = 0; my $sum_xij2 = 0; my $c_jiaozhengshu = 0; my $ss_t;
	for $i(0..@tmp-1){
		$sum_x += @tmp[$i];                                                 #就是按着书上公式算的，求总和
		$c_jiaozhengshu = ($sum_x* $sum_x) / @tmp;                          #书上的C值，总和的平方
		$sum_xij2+=(@tmp[$i] * @tmp[$i]);                                   #就是按着书上公式算的，求平方的总和                              
		$ss_t = $sum_xij2 - $c_jiaozhengshu;                                #书上的ss_T，
	}
		#print $ss_t,"\t";#$c_jiaozhengshu,"\t";
	my $sum_xi1 = 0; my $sum_xi2 = 0; my $sum_xi3 = 0 ;
	for $i(0..@tmp-1){
		if($a < 2.1){
			if (@tmp[$i] <= $a){
				$n1++;
				$sum_xi1 += @tmp[$i];#算的是每一组的和
			}
			elsif(@tmp[$i] > $a && @tmp[$i] <= $b ){
				$n2++;
				$sum_xi2 += @tmp[$i];
			}
			elsif(@tmp[$i] > $b){
				$n3++;
				$sum_xi3 += @tmp[$i];
			}
		}
		elsif($a > 2.1){                                                     #BBM model 只有两种类型
			if (@tmp[$i] <= $a){
				$n1++;
				$sum_xi1 += @tmp[$i];	  
			} 
			elsif(@tmp[$i] > $a ){
				$n2++;
				$sum_xi2 += @tmp[$i];
			}
		}		
	}
	#print "$n1\t$sum_xi1\t$n2\t$sum_xi2\t$n3\t$sum_xi3\t";
	#print "$n1\t$n2\t$n3\t";
	my $ss_chuli = 0; my $ss_e = 0; my $ms_chuli = 0; my $ms_e = 0; my $fprob = 0; my $f = 0;
	if ($n1!=0 && $n2!=0 && $n3!=0){
		$ss_chuli = (($sum_xi1 * $sum_xi1)/$n1 + ($sum_xi2 * $sum_xi2)/$n2 + ($sum_xi3 * $sum_xi3)/$n3) - $c_jiaozhengshu;
		$ss_e = $ss_t - $ss_chuli;                                 #$ss_chuli处理间差异，$ss_e处理内差异
		$ms_chuli = $ss_chuli/2;
		$ms_e = $ss_e/($sample_num-3);
		$f = sprintf"%.2f",$ms_chuli / $ms_e if $ms_e != 0;        #f值，这是分的三组，一共30个数，自由度分别是2,27
		$fprob=Statistics::Distributions::fprob (2, $sample_num-3, $f);         #由f值算出p值
		#print "$ss_t","\t","$ss_chuli","\t","$ss_e","\t","$ms_chuli","\t","$ms_e","\t","$f","\t","$fprob","\n";
		print "$fprob","\n";
	}
	elsif($n1==0 && $n2!=0 && $n3!=0){
		$ss_chuli = (($sum_xi2 * $sum_xi2)/$n2 + ($sum_xi3 * $sum_xi3)/$n3) - $c_jiaozhengshu;
		$ss_e = $ss_t - $ss_chuli;
		$ms_chuli = $ss_chuli;                                     #f值，这是分的两组组，一共30个数，自由度分别是1,28
		$ms_e = $ss_e/($sample_num-2) ;                                          
		$f = sprintf"%.2f",$ms_chuli / $ms_e if $ms_e != 0; 
		$fprob=Statistics::Distributions::fprob (1, $sample_num-2, $f);
		#print "$ss_t","\t","$ss_chuli","\t","$ss_e","\t","$ms_chuli","\t","$ms_e","\t","$f","\t","$fprob","\n";
		print "$fprob","\n";
	}	   
	elsif($n2==0 && $n1!=0 && $n3!=0){
		$ss_chuli = (($sum_xi1 * $sum_xi1)/$n1 + ($sum_xi3 * $sum_xi3)/$n3) - $c_jiaozhengshu;
		$ss_e = $ss_t - $ss_chuli;
		$ms_chuli = $ss_chuli;
		$ms_e = $ss_e/($sample_num-2);                                      #F_0.01 (1,28)= 7.636; F_0.05 (1,28)= 4.196; F_0.001 (1,28)= 13.498;
		$f = sprintf"%.2f",$ms_chuli / $ms_e if $ms_e != 0;
		$fprob=Statistics::Distributions::fprob (1, $sample_num-2, $f);
		#print "$ss_t","\t","$ss_chuli","\t","$ss_e","\t","$ms_chuli","\t","$ms_e","\t","$f","\t","$fprob","\n";
		print "$fprob","\n";
	}
	elsif($n3==0 && $n1!=0 && $n2!=0){
		$ss_chuli = (($sum_xi1 * $sum_xi1)/$n1 + ($sum_xi2 * $sum_xi2)/$n2) - $c_jiaozhengshu;
		$ss_e = $ss_t - $ss_chuli;
		$ms_chuli = $ss_chuli;
		$ms_e = $ss_e/($sample_num-2);
		$f = sprintf"%.2f",$ms_chuli / $ms_e if $ms_e != 0;
		$fprob=Statistics::Distributions::fprob (1, $sample_num-2, $f);
		#print "$ss_t","\t","$ss_chuli","\t","$ss_e","\t","$ms_chuli","\t","$ms_e","\t","$f","\t","$fprob","\n";
		print "$fprob","\n";
	}	   
	elsif($n1==0 && $n2==0 or $n2==0 && $n3==0 or $n1==0 && $n3==0){
		$ss_chuli = 0;                                                  #分成一组了，没法算f值了
		$f = 1;	 
		#$fprob = $f；
		#print "$ss_t","\t","$ss_chuli","\t","$ss_e","\t","$ms_chuli","\t","$ms_e","\t","$f","\t","1","\n";
		print "1","\n";                                                 #p值直接输出1了，方便fdr
	}
=cut
