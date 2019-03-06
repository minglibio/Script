# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Wed Mar  8 09:54:26 2017
@Mail: minnglee@163.com
@Author: Ming Li
"""

#从fasta文件中截取特定的序列

import sys
import os
import argparse
import time
import re
import gzip

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
def LoadFasta():
    Dict = {}
    seq = ''
    if args.GzFile:
        Fasta = gzip.open(args.fasta,'rb')
        for line in Fasta:
            StrLine = line.decode('GBK')
            StrLine = StrLine.strip()
            if StrLine[0] == '>':
                if len(seq) > 0:
                    Dict[name] = seq
                temp = StrLine.split()
                name = temp[0][1:]
                name = name.replace("chr","")
                seq = ''
            else:
                seq += StrLine
        Dict[name] = seq
    else:
        Fasta = open(args.fasta)
        for line in Fasta:
            line = line.strip()
            if line[0] == '>':
                if len(seq) > 0:
                    Dict[name] = seq
                temp = line.split()
                name = temp[0][1:]
                name = name.replace("chr","")
                print(name)
                seq = ''
            else:
                seq += line
        Dict[name] = seq
    return Dict
def GetSeqFromBed():
    FastaDict = LoadFasta()
    for line in args.bed:
        if line.startswith('#'):continue
        line = line.strip().split()
        line[0] = line[0].replace("chr","")
        name = "{0}:{1}-{2}".format(line[0],line[1],line[2])
        args.output.write(">{0}\n{1}\n".format(name,FastaDict[line[0]][int(line[1])-1:int(line[2])]))
def main():
    print('Running...')
    log('The start time: {0}'.format(time.ctime()))
    log('The command line is:\n{0}'.format(GetCommandLine()))
    GetSeqFromBed()
    log('The end time: {0}'.format(time.ctime()))
    print('Done!')
#############################Argument
parser = argparse.ArgumentParser(description=print(__doc__),formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-f','--fasta',metavar='File',dest='fasta',help='Fasta file',type=str,required=True)
parser.add_argument('-g','--GzFile',dest='GzFile',help='The input is gz file',action='store_true',default=False)
parser.add_argument('-b','--bed',metavar='File',dest='bed',help='Bed file',type=open,required=True)
parser.add_argument('-o','--Output',metavar='File',dest='output',help='Output file',type=argparse.FileType('w'),required=True)
args = parser.parse_args()
###########################
if __name__ == '__main__':
    main()
