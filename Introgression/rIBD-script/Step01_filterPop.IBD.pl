open f3,"<../Allchicken.chr$ARGV[0].filter4_final_no3_MAF005.Phase.ibd40.ibdlod1.ibd";
open f1,"<68ggm.list";
open f2,"<indiaDC.list";
open f4,">68ggm-indiaDC.Allchicken.chr$ARGV[0].filter4_final_no3_MAF005.Phase.ibd40.ibdlod1.ibd";
while(<f1>){
   chomp;
   $hash1{$_}=1;
  }

 while(<f2>){
   chomp;
   $hash2{$_}=1;
  }

while(<f3>){
   chomp;
   $line=$_;
   @aa=split(/\s+/,$line);
   if((exists$hash1{$aa[0]}) and (exists$hash2{$aa[2]})){
     print f4"$line\n";
      }
   elsif((exists$hash2{$aa[0]}) and (exists$hash1{$aa[2]})){
     print f4"$line\n";
    }
  }

close f1,f2,f3,f4;
  
