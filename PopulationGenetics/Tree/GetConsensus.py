# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Mon Sep 18 16:14:07 2017
@Mail: minnglee@163.com
@Author: Ming Li
"""

import sys
import os
import argparse
import time
import re

def GetCommandLine():
    CommandLine = 'python3 {0}'.format(' '.join(sys.argv))
    return(CommandLine)
LogFile = None
def log(LogInfo):
    '''
    Output the LogInfo to log file
    '''
    global LogFile
    if sys.platform == 'linux':
        CurrentFolder = os.getcwd()
        LogFileName = re.split('/|\\\\',sys.argv[0].strip())
        LogFileName = LogFileName[-1].split('.')
        LogFileName = '{0}/{1}.log'.format(CurrentFolder,LogFileName[0])
        if LogFile: LogFile.write(LogInfo+'\n')
        else:
            LogFile = open(LogFileName,'w')
            LogFile.write(LogInfo+'\n')
    else:
        print(LogInfo)
def LoadNameDict():
    '''
    A1      A1      M       EUR     FRCH05  WEST    EUR
    A14     A14     F       IRN     IRCH21  IRN     IRN
    A23     A23     F       IRN     IRCH23  IRN     IRN
    '''
    Dict = {}
    for line in args.Name:
        line = line.strip().split()
        Dict[line[4]] = line[0]
    return Dict
def Output(seq):
    Sequence = ''
    seq = seq.split('\n')
    for line in seq:
        if len(line) == 0:continue
        if line[0] == '>':continue
        else:
            Sequence += line
    return Sequence
Ref = '~/ref/goat/ASM.fa'
Region = '29:46245000-46248500'
VCF = '~/01.Goat/05.vcf/02.Imputation_And_Phase/29.phase.vcf.gz'
def GetConsensus():
    NameDict = LoadNameDict()
    OutputList = []
    SampleOrder = 1
    for line in args.sample:
        line = line.strip()
        Seq = os.popen('samtools faidx {ref} {region} |bcftools consensus -H 1 -s {sample} {vcf}'.format(ref=Ref,region=Region,sample=NameDict[line],vcf=VCF)).read()
        Name = '{0}-1^{1}'.format(line,SampleOrder)
        OutputList.append([Name,Output(Seq)])
        SampleOrder += 1
        Seq = os.popen('samtools faidx {ref} {region} |bcftools consensus -H 2 -s {sample} {vcf}'.format(ref=Ref,region=Region,sample=NameDict[line],vcf=VCF)).read()
        Name = '{0}-2^{1}'.format(line,SampleOrder)
        OutputList.append([Name,Output(Seq)])
        SampleOrder += 1
    SampleNum = len(OutputList)
    SeqLen = len(OutputList[0][1])
    args.output.write('{0} {1}\n'.format(SampleNum,SeqLen))
    for seq in OutputList:
        args.output.write('{0}    {1}\n'.format(seq[0],seq[1]))
def main():
    print('Running...')
    log('The start time: {0}'.format(time.ctime()))
    log('The command line is:\n{0}'.format(GetCommandLine()))
    GetConsensus()
    log('The end time: {0}'.format(time.ctime()))
    print('Done!')
#############################Argument
parser = argparse.ArgumentParser(description=print(__doc__),formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-s','--sample',metavar='File',dest='sample',help='Sample List file',type=open,required=True)
parser.add_argument('-n','--Name',metavar='File',dest='Name',help='Name file',type=open,required=True)
parser.add_argument('-o','--Output',metavar='File',dest='output',help='Output file',type=argparse.FileType('w'),required=True)
args = parser.parse_args()
###########################
if __name__ == '__main__':
    main()
