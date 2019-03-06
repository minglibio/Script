#!/bin/bash
:>SweeD_Report
for i in {{1..26},X}
do
cat SweeD_Report.${i} |sed s#//1#//${i}#g >> SweeD_Report
done
