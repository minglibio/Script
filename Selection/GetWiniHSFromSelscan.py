# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Tue Dec 12 15:01:40 2017
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
def LoadiHS():
    '''
    chr1:5192       5192    0.383333        4326.89 1032.91 1.43247 0.779637        0
    chr1:6030       6030    0.0666667       2570.08 664.993 1.35192 -0.277839       0
    chr1:6074       6074    0.35    2858.67 128.586 3.10152 1.85933 0
    '''
    Dict = {}
    ChrSet = set()
    next(args.input)
    for line in args.input:
        line = line.strip().split()
        Position = line[0].split(':')
        Chr = int((Position[0].replace('chr',''))[0])
        Dict.setdefault(Chr,[]).append([int(Position[1]),float(line[-1])])
        ChrSet.add(Chr)
    return Dict,ChrSet
def ReturnSlideWindowIndex(start,end,LastIndex,DictList):
    List=[]
    index=LastIndex
    try:
        for i in range(LastIndex,end):
            if DictList[i][0] <= start+args.step:
                List.append(DictList[i][1])
                index=i+1
            elif DictList[i][0] <= end:
                List.append(DictList[i][1])
            else:
                break
        return List,index,True
    except IndexError:
        return List,index,False
def CalculateWindow(List,StartIndex):
    SnpNum=len(List)
#    print(List)
    if SnpNum==0:
        StartIndex-=1
        return 0,0,StartIndex
    else:
        ValidiHSNum = 0
        for i in List:
            if abs(i) >= 2:
                ValidiHSNum += 1
        return SnpNum,ValidiHSNum/SnpNum,StartIndex
def GetWiniHSFromSelscan():
    args.output.write('CHR\tSTART\tEND\tSnpNum\tWiniHS\n')
    iHSDict,ChrSet = LoadiHS()
    print('iHS loaded!')
    for CHR in ChrSet:
        end = args.window
        start = 0
        StartIndex = 0
        NotEnd = True
        while NotEnd :
            WinSnpList,StartIndex,NotEnd = ReturnSlideWindowIndex(start,end,StartIndex,iHSDict[CHR])
            SnpNum,WiniHS,StartIndex = CalculateWindow(WinSnpList,StartIndex)
            args.output.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(CHR,start,end,SnpNum,WiniHS))
            start += args.step
            end += args.step
def main():
    print('Running...')
    log('The start time: {0}'.format(time.ctime()))
    log('The command line is:\n{0}'.format(GetCommandLine()))
    GetWiniHSFromSelscan()
    log('The end time: {0}'.format(time.ctime()))
    print('Done!')
#############################Argument
parser = argparse.ArgumentParser(description=print(__doc__),formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i','--Input',metavar='File',dest='input',help='Input file',type=open,required=True)
parser.add_argument('-w','--Window',metavar='Int',dest='window',help='Slide Window Size',type=int,default=40000)
parser.add_argument('-s','--Step',metavar='Int',dest='step',help='Step Size',type=int,default=10000)
parser.add_argument('-o','--Output',metavar='File',dest='output',help='Output file',type=argparse.FileType('w'),required=True)
args = parser.parse_args()
###########################
if __name__ == '__main__':
    main()
