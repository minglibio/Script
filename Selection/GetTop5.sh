#!/bin/bash
if [ $# -ne 2 ]; then
 echo "error.. need args"
 echo "command:$0 <File> <Column>"
 exit 1
fi
File=$1
Column=$2
TotalLine=`wc -l ${File}|awk '{print $1}'`
Top=`AA=${TotalLine};BB=100;echo "scale=0;${AA}/${BB}*5"|bc`
sort -k ${Column} -r -g ${File} |head -${Top} > ${File}.top5
