#`sort -nk6 Allchicken.chr16.filter4_final_no3.ibd.ibd`;
open f1,"<68ggm-indiaDC.Allchicken.chr$ARGV[0].filter4_final_no3_MAF005.Phase.ibd40.ibdlod1.ibd";
open f2,">68ggm-indiaDC.Allchicken.chr$ARGV[0].IBD.freq.txt";

while(<f1>){
  chomp;
  #100S    2       107S_L2_I031    2       16      136613  149306  3.78
  @aa=split(/\s+/,$_);  
   for($i=$aa[5];$i<=$aa[6];$i++){
       $hash{$i}++;
   }
 }

$all_com=$ARGV[1];
@key=sort{$a <=> $b}(keys%hash);
   #$freq=$hash{$key}/$all_com;
  foreach $key(@key){ ##key is position
   $freq=$hash{$key}/$all_com;
   print f2"$ARGV[0]\t$key\t$freq\t$hash{$key}\n";
  } 
