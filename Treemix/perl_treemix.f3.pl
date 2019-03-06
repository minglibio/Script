open f1,"<../data.clust";
open f2,"<../Green_Ggm2Dom.txt";
#open f3,">Green_Ggm_Dom.clust";
#open pbs,"";
while (<f1>){
  chomp;
  @aa=split(/\s+/,$_);
  $hash{$aa[1]}=$aa[2];
}
 
@keys=keys %hash;

while(<f2>){
  chomp;
  @bb=split(/\s+/,$_);
 open f3,">Green_Ggm_$bb[2].clust";
 open pbs,">PBS_treemix_Green_Ggm_$bb[2]"; 
 print pbs"#!/bin/sh\n#PBS -N $bb[2]\n#PBS -q long\n#PBS -l nodes=1:ppn=1\n#PBS -o $bb[2].out\n#PBS -e $bb[2].err\n cd /lustre/user/liyan/WangMS/Global_chicken/GA_project_snp_without/f3test_citygroup/Green_Ggm2Dom\n/lustre/user/liyan/WangMS/software/plink_1.9/plink --bfile /lustre/user/liyan/WangMS/Global_chicken/GA_project_snp_without/f3test/Global_chicken_without.no3_autos_prunedData_pairwise --dog --freq --missing --within Green_Ggm_$bb[2].clust --out Green_Ggm_$bb[2]\ngzip Green_Ggm_$bb[2].frq.strat\n /lustre/user/liyan/WangMS/software/treemix-1.2/plink2treemix.py Green_Ggm_$bb[2].frq.strat.gz Green_Ggm_$bb[2].frq.gz\n/lustre/user/liyan/WangMS//software/treemix-1.2/bin/threepop -i Green_Ggm_$bb[2].frq.gz -k 500 >Green_Ggm_$bb[2].f3.txt\nrm Green_Ggm_$bb[2].frq.strat.gz Green_Ggm_$bb[2].frq.gz\n";
  foreach $i(@keys){
    if(($hash{$i} eq $bb[0]) or ($hash{$i} eq $bb[1]) or ($hash{$i} eq $bb[2])){
    
     print f3"$i\t$i\t$hash{$i}\n";
   }
  }
  close f3,pbs;
 }
