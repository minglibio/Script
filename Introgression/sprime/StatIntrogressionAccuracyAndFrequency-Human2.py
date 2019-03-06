# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Wed May  9 23:06:31 2018
@Mail: minnglee@163.com
@Author: Ming Li
"""

import sys,os,argparse,time,re
import gzip

def GetCommandLine():
    CommandLine='python3 {0}'.format(' '.join(sys.argv))
    return(CommandLine)
LogFile=None
def log(LogInfo):
    '''
    Output the LogInfo to log file
    '''
    global LogFile
    if sys.platform == 'linux':
        CurrentFolder=os.getcwd()
        LogFileName=re.split('/|\\\\',sys.argv[0].strip())
        LogFileName=LogFileName[-1].split('.')
        LogFileName='{0}/{1}.log'.format(CurrentFolder,LogFileName[0])
        if LogFile:LogFile.write(LogInfo+'\n')
        else:
            LogFile=open(LogFileName,'w')
            LogFile.write(LogInfo+'\n')
    else:
        print(LogInfo)
def LoadIntro(FILE):
    '''
    2694047.4       2694336.3       207     208     218     231     237     239
    2694336.3       2694397.0       207     208     218     231     237     239
    2694397.0       2694454.2       207     208     218     231     237     239
    '''
    IntroList = []
    IntroLen = 0
    for line in FILE:
        line = line.strip().split()
        IntroList.append(line)
#        IntroLen += (float(line[1]) - float(line[0])) * (len(line) - 2)
    return IntroList,IntroLen
def LoadVCF(FileName,PosDict):
    Dict = {}
    GzFile = True
    if GzFile:
        INPUT = gzip.open(FileName,'rb')
        GzFile = True
    else: 
        INPUT = open(FileName)
    
    for line in INPUT:
        if GzFile: line = line.decode()
        if line.startswith('#'): continue
        else:
            line = line.strip().split()
            if not line[1] in PosDict: continue
            AlleleList = []
            for i in range(9,len(line)):
                Allele = line[i].split('|')
                AlleleList.extend(Allele)
            Dict[line[1]] = AlleleList
    return Dict
def IfIntro(IntroAllele,HapList,HapAllele):
    Intro = True
    for hap in HapList:
#        print(hap)
        if HapAllele[int(hap)] != IntroAllele: Intro = False
    return Intro
def StatIntrogressionAccuracyAndFrequency(iterate,IntroLen,TrueIntrogressiveVar,FalseIntrogressiveVar):
    '''
    CHROM   POS     ID      REF     ALT     SEGMENT ALLELE  SCORE
    1       2694307 .       A       T       0       1       238280
    1       2694907 .       A       T       0       0       238280
    1       2695139 .       A       T       0       1       238280
    '''
    SCORE = open('{0}HumanSimulation.i{1}.vcf.gz.out.score'.format(args.fragment,iterate))
    ScoreList = []
    ScoreDict = {}
    for line in SCORE:
        if line.startswith('CHROM'): continue
        line = line.strip().split()
        ScoreList.append(line[1])
        ScoreDict[line[1]] = line[6]
    TrueIntroFile = open('{0}HumanSimulation.i{1}.intro'.format(args.intro,iterate))
    AlleleDict = LoadVCF('{0}HumanSimulation.i{1}.vcf.gz'.format(args.intro,iterate), ScoreDict)
    TrueIntroList,FileIntroLen = LoadIntro(TrueIntroFile)
    TrueIntroSet = set()
    
    for pos in ScoreList:
        TrueIntro = False
        NeedPop = False
        PopNum = 0
        for TrueIntroSegm in TrueIntroList:
            if float(TrueIntroSegm[0]) <= int(pos) <= float(TrueIntroSegm[1]):
                Intro = IfIntro(ScoreDict[pos],TrueIntroSegm[2:],AlleleDict[pos])
                if Intro:
                    TrueIntrogressiveVar += 1
                    TrueIntroSet.add('\t'.join(TrueIntroSegm))
                    TrueIntro = True
                break
            elif int(pos) < float(TrueIntroSegm[1]):
                break
            elif int(pos) > float(TrueIntroSegm[1]):
                NeedPop = True
                PopNum +=1
        if NeedPop:
            for i in range(PopNum):
                TrueIntroList.pop(0)
        if not TrueIntro: FalseIntrogressiveVar += 1
    for TrueIntroSegm in TrueIntroSet:
        TrueIntroSegm = TrueIntroSegm.strip().split()
        IntroLen += (float(TrueIntroSegm[1]) - float(TrueIntroSegm[0])) * (len(TrueIntroSegm) - 2)
    return IntroLen,TrueIntrogressiveVar,FalseIntrogressiveVar
def Running():
    args.output.write('TotalLen\tIntroLen\tTrueIntrogressiveVar\tFalseIntrogressiveVar\n')
    IndNum = 800
    Len = 10000000
    TotalLen = 0
    IntroLen = 0
    TrueIntrogressiveVar = 0
    FalseIntrogressiveVar = 0
    for iterate in range(1,args.iterate+1):
        TotalLen += Len*IndNum
        IntroLen,TrueIntrogressiveVar,FalseIntrogressiveVar = StatIntrogressionAccuracyAndFrequency(iterate,IntroLen,TrueIntrogressiveVar,FalseIntrogressiveVar)
    args.output.write('{0}\t{1}\t{2}\t{3}\n'.format(TotalLen,IntroLen,TrueIntrogressiveVar,FalseIntrogressiveVar))
def main():
    print('Running...')
    log('The start time: {0}'.format(time.ctime()))
    log('The command line is:\n{0}'.format(GetCommandLine()))
    Running()
    log('The end time: {0}'.format(time.ctime()))
    print('Done!')
#############################Argument
parser=argparse.ArgumentParser(description=print(__doc__),formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-f','--fragment',metavar='File',dest='fragment',help='Tne path of introgression fragment file',type=str,required=True)
parser.add_argument('-i','--intro',metavar='File',dest='intro',help='Tne path of intro file',type=str,required=True)
parser.add_argument('--iterate',metavar='Ind',dest='iterate',help='The number of iterate(seed) (default:100)',type=int,default=100)
parser.add_argument('-o','--Output',metavar='File',dest='output',help='Output file',type=argparse.FileType('w'),required=True)
args=parser.parse_args()
###########################
if __name__=='__main__':
    main()