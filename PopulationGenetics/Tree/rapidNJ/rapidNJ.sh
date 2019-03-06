#!/bin/bash
if [ $# -ne 4 ]; then
 echo "error.. need args"
 echo "command:$0 <Input file[FASTA]> <bootstrap> <Thread> <Prefix of output>"
 exit 1
fi
InFile=$1
BootStrap=$2
Thread=$3
Prefix=$4
rapidnj ${InFile} -b ${BootStrap} -c ${Thread} -x ${Prefix}.nwk
