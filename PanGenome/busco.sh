#!/bin/bash
if [ $# -ne 1 ]; then
 echo "error.. need args"
 echo "command: $0 <Fasta file>"
 exit 1
fi

export PATH="/stor9000/apps/users/NWSUAF/2015050469/anaconda3/bin:$PATH"
export PATH="/stor9000/apps/users/NWSUAF/2015050469/software/Augustus-master/bin:$PATH"
export PATH="/stor9000/apps/users/NWSUAF/2015050469/software/Augustus-master/scripts:$PATH"
export AUGUSTUS_CONFIG_PATH="/stor9000/apps/users/NWSUAF/2015050469/software/Augustus-master/config"
export LD_LIBRARY_PATH=/stor9000/apps/users/NWSUAF/2015050469/software/lp_solve_5.5/lpsolve55/bin/ux64:$LD_LIBRARY_PATH

Fasta=$1
python3 ~/anaconda3/bin/run_BUSCO.py --in ${Fasta} --out out --lineage_path ~/software/busco/db/Eukaryota/aves_odb9 --mode genome -f -c 24 -sp chicken
