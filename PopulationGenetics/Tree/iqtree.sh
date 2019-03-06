#!/bin/bash
if [ $# -ne 4 ]; then
 echo "error.. need args"
 echo "command: $0 <Input file[PHYLIP/FASTA/NEXUS/CLUSTAL/MSF]> <Outgroup name> <Thread> <Prefix of output>"
 exit 1
fi
InFile=$1
OutGroup=$2
Thread=$3
Prefix=$4
iqtree -s ${InFile} -nt ${Thread} -bb 1000 -m TEST -o ${OutGroup} -pre ${Prefix}
