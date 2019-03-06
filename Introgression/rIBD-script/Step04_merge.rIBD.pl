open f1,"<ggsp-705DC.Allchicken.allchr.IBD.freq.sort.W10K.S5K.txt";
#open f2,"<SilyJF-SrilanlaDC.W20k.s10K.all.freq.txt";
open f2,"<Grey-705DC.Allchicken.allchr.IBD.freq.sort.W10K.S5K.txt";
open f3,"<Grey-ggsp-705DC.Allchicken.allchr.IBD.freq.sort.W10K.S5K.pos.txt";
open f4,">Grey-ggsp-705DC.rIBD.freq.txt";

print f4"CHR\tPOS\trIBD(ggsp-Grey)\n";
#@f1=<f1>;
while(<f1>){
  @aa=split(/\s+/,$_);
  $hash1{$aa[0]}{$aa[1]}=$aa[2];
 }

while(<f2>){
  @aa=split(/\s+/,$_);
  $hash2{$aa[0]}{$aa[1]}=$aa[2];
 }

 while(<f3>)
  {
  chomp;
  @cc=split(/\s+/,$_);
   if(exists $hash1{$cc[0]}{$cc[1]})
  {
   ;
  }
 else{
  $hash1{$cc[0]}{$cc[1]}=0;
 }

  if(exists $hash2{$cc[0]}{$cc[1]})
  {
   ;
  }
 else{
  $hash2{$cc[0]}{$cc[1]}=0;
 }

  $rbd=$hash1{$cc[0]}{$cc[1]}-$hash2{$cc[0]}{$cc[1]};
  print f4"$cc[0]\t$cc[1]\t\t$rbd\n";
   $rbd=0;
}

 
