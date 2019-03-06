#perl -lane 'next if $_!~/Once/;@F=split/NNNNNN/,$_;$link2 = ($_ =~ s/link-link2/A/g);$link3 = ($_ =~ s/link-link2\:/A/g);$link3 = ($_ =~ s/link-link-link3\:/A/g);@A=split/\s+/,$F[1];@B=split/\s+/,$F[2];print "$F[0]\t\t","$A[-3]\t$A[-2]\t$A[-1]","\t\t$B[-3]\t$B[-2]\t$B[-1]","\t\t$link2\t$link3";'  /home/jiangyu/xiaoming/tianxiaomeng/out/test/out >/home/jiangyu/xiaoming/tianxiaomeng/out/test/out2
#####将novel定位分为两个文件
#out 为上一步输出
#out1 为直接定位到常染色体
#out2 为间接定位到Novel，后通过Novel定位到常染色体
export a=$1
export b=$2
export c=$3

perl -le 'open(IN1, "$ARGV[0]");open(IN2, ">$ARGV[1]");open(IN3, ">$ARGV[2]");while(<IN1>){next if $_!~/Once/;@F=split/NNNNNN/,$_;$link2 = ($_ =~ s/link-link2\:/A/g);$link3 = ($_ =~ s/link-link-link3\:/A/g);@A=split/\s+/,$F[1];@B=split/\s+/,$F[2];if($#F==1){print IN2  "$F[0]\t$A[-3]\t$A[-2]\t$A[-1]";}else{if($F[1]=~/PASS|link\<3/){print  IN3 "$F[0]\t$B[-3]\t$B[-2]\t$B[-1]";}elsif($F[2]=~/PASS|link\<3/){print IN3 "$F[0]\t$A[-3]\t$A[-2]\t$A[-1]";}else{print  IN3 "$F[0]\t$B[-3]\t$B[-2]\t$B[-1]\t$A[-3]\t$A[-2]\t$A[-1]";}}}'  $a $b $c
