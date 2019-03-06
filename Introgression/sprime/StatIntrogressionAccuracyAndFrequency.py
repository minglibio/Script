# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Mon Apr 23 19:55:50 2018
@Mail: minnglee@163.com
@Author: Ming Li
"""

import sys,os,argparse,time,re

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
        IntroLen += (float(line[1]) - float(line[0])) * (len(line) - 2)
    return IntroList,IntroLen
def StatIntrogressionAccuracyAndFrequency(iterate,TotalIntroLen,IntroLen,TrueIntrogressiveVar,FalseIntrogressiveVar):
    '''
    CHROM   POS     ID      REF     ALT     SEGMENT ALLELE  SCORE
    1       2694307 .       A       T       0       1       238280
    1       2694907 .       A       T       0       0       238280
    1       2695139 .       A       T       0       1       238280
    '''
    SCORE = open('{0}GoatSimulation.i{1}.R1e-08.out.score'.format(args.fragment,iterate))
    Intro = open('{0}GoatSimulation.i{1}.R1e-08.intro'.format(args.intro,iterate))
    IntroList,FileIntroLen = LoadIntro(Intro)
    TotalIntroLen += FileIntroLen
    TrueIntroSet = set()
    '''
    TrueIntrogressiveVar = 0
    FalseIntrogressiveVar = 0
    TrueIntroSet = set()
    SCORE=[1,2,5,9,15,20,28,30,35,38,40]
#    SCORE=[15,16,20]
    IntroList=[['4.99','10.0'],[11,12],[12,13],[13.0,14.0],[14,14.5],['19.0','30.0']]
    for pos in SCORE:
        TrueIntro = False
        NeedPop = False
        PopNum = 0
        for intro in IntroList:
#            print(pos,intro)
            if float(intro[0]) <= pos <= float(intro[1]):
                TrueIntrogressiveVar += 1
                print('true',pos)
                TrueIntroSet.add('\t'.join(intro))
                TrueIntro = True
                break
            elif pos < float(intro[0]):
                FalseIntrogressiveVar += 1
                TrueIntro = True
                print('false',pos)
                break
            elif pos > float(intro[1]):
                NeedPop = True
                PopNum +=1
#                print(len(IntroList))
        if NeedPop:
            for i in range(PopNum):
                IntroList.pop(0)
        if not TrueIntro: 
            FalseIntrogressiveVar += 1
            print('false-1',pos)
#        print(IntroList)
        print()
    print(TrueIntrogressiveVar,FalseIntrogressiveVar)
    '''
    for line in SCORE:
        if line.startswith('CHROM'): continue
        line = line.strip().split()
        TrueIntro = False
        NeedPop = False
        PopNum = 0
        for intro in IntroList:
            if float(intro[0]) <= int(line[1]) <= float(intro[1]):
                TrueIntrogressiveVar += 1
                TrueIntroSet.add('\t'.join(intro))
                TrueIntro = True
                break
            elif int(line[1]) < float(intro[1]):
                FalseIntrogressiveVar += 1
                TrueIntro = True
                break
            elif int(line[1]) > float(intro[1]):
                NeedPop = True
                PopNum +=1
        if NeedPop:
            for i in range(PopNum):
                IntroList.pop(0)
        if not TrueIntro: FalseIntrogressiveVar += 1
    for intro in TrueIntroSet:
        intro = intro.strip().split()
        IntroLen += (float(intro[1]) - float(intro[0])) * (len(intro) - 2)
    return TotalIntroLen,IntroLen,TrueIntrogressiveVar,FalseIntrogressiveVar
def Running():
    args.output.write('TotalLen\tTotalIntroLen\tIntroLen\tTrueIntrogressiveVar\tFalseIntrogressiveVar\n')
    IndNum = 800
    Len = 10000000
    TotalLen = 0
    IntroLen = 0
    TotalIntroLen = 0
    TrueIntrogressiveVar = 0
    FalseIntrogressiveVar = 0
    for iterate in range(1,args.iterate+1):
        TotalLen += Len*IndNum
        TotalIntroLen,IntroLen,TrueIntrogressiveVar,FalseIntrogressiveVar = StatIntrogressionAccuracyAndFrequency(iterate,TotalIntroLen,IntroLen,TrueIntrogressiveVar,FalseIntrogressiveVar)
    args.output.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(TotalLen,TotalIntroLen,IntroLen,TrueIntrogressiveVar,FalseIntrogressiveVar))
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