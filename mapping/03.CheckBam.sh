#!/bin/bash
if [ $# -ne 1 ]; then
 echo "error.. need args"
 echo "command: $0 <Path>"
 exit 1
fi
Path=$1
######
FileList=`ls -al ${Path}/*.bam |awk '{print $9}'`
for File in ${FileList}
do
echo ${File}
samtools flagstat ${File} &
Time1=`date +%s`
Time2=`date +%s`
i=$((${Time2} - ${Time1}))
while [[ "${i}" -ne "3" ]]
do
    Time2=`date +%s`
    i=$((${Time2} - ${Time1}))
done
kill $!
done
