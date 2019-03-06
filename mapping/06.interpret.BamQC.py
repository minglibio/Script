# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Tue Jul 24 16:33:12 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import re

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-p','--path',type=str,help='The path of BAM stat file',required=True)
@click.option('-o','--output',type=str,help='The name of output file',default='BamStat.results')
def main(path,output):
    FileList = os.popen(f'find {path} -name genome_results.txt|sort')
    OUTPUT = open(output,'w')
    OUTPUT.write(f'Sample\tTotal reads\tMapped reads\tMapping rate\tDuplication\tInsert size\tmapping quality\tDepth\t1X\t2X\t3X\t4X\n')
    for File in FileList:
        File = File.strip()
        FileName = File.split('/')[-2]
        print(File)
        OUTPUT.write(f'{FileName}\t')
        INPUT = open(File,'r')
        for line in INPUT:
            line = line.strip()
            if re.search('number of reads =',line):
                AA = re.search('(?<=number of reads = ).*',line).group() 
                OUTPUT.write(f"{AA}\t")
            if re.search('number of mapped reads =',line):
                AA = re.search('(?<=number of mapped reads = ).*(?= \()',line).group()
                OUTPUT.write(f"{AA}\t")
            if re.search('mean mapping quality =',line):
                AA = re.search('(?<=mean mapping quality = ).*',line).group()
                print (AA)
                OUTPUT.write(f"{AA}\t")
            if re.search('mean coverageData =',line):
                AA = re.search('(?<=mean coverageData = ).*',line).group()
                OUTPUT.write(f"{AA}\t")
            if re.search('median insert size =',line):
                AA = re.search('(?<=median insert size = ).*',line).group()
                OUTPUT.write(f"{AA}\t")
            if re.search('number of mapped reads =',line):
                AA = re.search('(?<=\().*(?=\))',line).group()
                OUTPUT.write(f"{AA}\t")
            if re.search('duplication rate =',line):
                AA = re.search('(?<=duplication rate = ).*',line).group()
                OUTPUT.write(f"{AA}\t")
            if re.search('reference with a coverageData >= 1X',line):
                AA = re.search('(?<=There is a ).*(?= of reference)',line).group()
                OUTPUT.write(f"{AA}\t")
            if re.search('reference with a coverageData >= 2X',line):
                AA = re.search('(?<=There is a ).*(?= of reference)',line).group()
                OUTPUT.write(f"{AA}\t")
            if re.search('reference with a coverageData >= 3X',line):
                AA = re.search('(?<=There is a ).*(?= of reference)',line).group()
                OUTPUT.write(f"{AA}\t")
            if re.search('reference with a coverageData >= 4X',line):
                AA = re.search('(?<=There is a ).*(?= of reference)',line).group()
                OUTPUT.write(f"{AA}\t")
        OUTPUT.write(f'\n')
if __name__ == '__main__':
    main()
