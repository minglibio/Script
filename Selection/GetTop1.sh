#!/bin/bash
if [ $# -ne 3 ]; then
 echo "error.. need args"
 echo "command:$0 <File> <Column> <Output>"
 exit 1
fi
File=$1
Column=$2
Out=$3
TotalLine=`wc -l ${File}|awk '{print $1}'`
Top=`AA=${TotalLine};BB=100;echo "scale=0;${AA}/${BB}"|bc`
sort -k ${Column} -r -g ${File} |head -${Top}  > ${Out}.top1
