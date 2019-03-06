#!/bin/bash
#!/bin/bash
if [ $# -ne 4 ]; then
 echo "error.. need args"
 echo "command: $0 <Input file[PHYLIP]> <Outgroup name> <Prefix of output> <Threads>"
 exit 1
fi
PhylipFile=$1
Outgroup=$2
OutName=$3
Threads=$4
raxmlHPC-PTHREADS -f a -x 123 -p 23 -# 100 -k -s ${PhylipFile} -m GTRGAMMA -n ${OutName} -T ${Threads} -o ${Outgroup}
