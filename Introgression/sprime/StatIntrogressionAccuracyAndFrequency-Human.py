# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Mon Apr 23 19:55:50 2018
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
def LoadIntrogressionFragment(FILE):
    '''
    CHROM   POS     ID      REF     ALT     SEGMENT ALLELE  SCORE
    9       6624    .       C       T       12      1       2710303
    9       6821    .       A       G       12      1       2710303
    9       6936    .       G       A       12      1       2710303
    '''
    SegmentDict = {}
    for line in FILE:
        if line.startswith('CHROM'): continue
        line = line.strip().split()
        SegmentDict[line[1]] = line[6]
    return SegmentDict
def LoadSample(File):
    Dict = {}
    FILE = open(File)
    for line in FILE:
        line = line.strip()
        Dict[line] = None
    return Dict
def HandleHeader(line):
    SampleDict = LoadSample(args.Sample)
    OutgroupDict = LoadSample(args.Outgroup)
    SampleIndex,OutgroupIndex = [],[]
    line = line.strip().split()
    for i in range(4,len(line)):
        if line[i] in SampleDict:
            SampleIndex.append(line.index(line[i]))
        elif line[i] in OutgroupDict:
            OutgroupIndex.append(line.index(line[i]))
    return SampleIndex,OutgroupIndex
def StatIntrogressionAccuracyAndFrequency(iterate,TotalVar,TotalIntrogressiveVar,TrueIntrogressiveVar,FalseIntrogressiveVar):
    GzFile = False
    if args.GzFile:
        VCF = gzip.open('{0}HumanSimulation.i{1}.vcf.gz'.format(args.vcf,iterate),'rb')
        GzFile = True
    else: 
        VCF = open('{0}HumanSimulation.i{1}.vcf'.format(args.vcf,iterate))
    SCORE = open('{0}HumanSimulation.i{1}.vcf.gz.out.score'.format(args.fragment,iterate))
    SegmentDict = LoadIntrogressionFragment(SCORE)
    for line in VCF:
        if GzFile: line = line.decode()
        line = line.strip()
        if line.startswith('##'): continue
        if line.startswith('#CHROM'):
            SampleIndex,OutgroupIndex = HandleHeader(line)
#            print(SampleIndex,OutgroupIndex)
            continue
        else:
            line = line.strip().split()
            TotalVar += (len(line)-9)*2
            if line[1] not in SegmentDict: continue
            TotalIntrogressiveVar += (len(line)-9)*2
            OutgroutVar = 0
            for i in OutgroupIndex:
                if line[i] == '0|1' or line[i] == '1|0':
                    OutgroutVar += 1
                elif line[i] == '1|1':
                    OutgroutVar += 2
            if SegmentDict[line[1]] == '0' and OutgroutVar != (len(line)-9)*2:
#                print(222)
                for i in SampleIndex:
                    if line[i] == '0|0':
                        TrueIntrogressiveVar += 2
                    elif line[i] == '0|1' or line[i] == '1|0':
                        TrueIntrogressiveVar += 1
            elif SegmentDict[line[1]] == '0' and OutgroutVar == (len(line)-9)*2:
#                print(333)
                for i in SampleIndex:
                    if line[i] == '0|0':
                        FalseIntrogressiveVar += 2
                    elif line[i] == '0|1' or line[i] == '1|0':
                        FalseIntrogressiveVar += 1
            elif SegmentDict[line[1]] == '1' and OutgroutVar != 0:
#                print(444)
                for i in SampleIndex:
                    if line[i] == '1|1':
                        TrueIntrogressiveVar += 2
                    elif line[i] == '0|1' or line[i] == '1|0':
                        TrueIntrogressiveVar += 1
            elif SegmentDict[line[1]] == '1' and OutgroutVar == 0:
#                print(555)
                for i in SampleIndex:
                    if line[i] == '1|1':
                        FalseIntrogressiveVar += 2
                    elif line[i] == '0|1' or line[i] == '1|0':
                        FalseIntrogressiveVar += 1
    return TotalVar,TotalIntrogressiveVar,TrueIntrogressiveVar,FalseIntrogressiveVar
def Running():
    args.output.write('TotalVar\tTotalIntrogressiveVar\tTrueIntrogressiveVar\tFalseIntrogressiveVar\n')
    TotalVar = 0
    TotalIntrogressiveVar = 0
    TrueIntrogressiveVar = 0
    FalseIntrogressiveVar = 0
    for iterate in range(1,args.iterate+1):
        TotalVar,TotalIntrogressiveVar,TrueIntrogressiveVar,FalseIntrogressiveVar = StatIntrogressionAccuracyAndFrequency(iterate,TotalVar,TotalIntrogressiveVar,TrueIntrogressiveVar,FalseIntrogressiveVar)
    args.output.write('{0}\t{1}\t{2}\t{3}\n'.format(TotalVar,TotalIntrogressiveVar,TrueIntrogressiveVar,FalseIntrogressiveVar))
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
parser.add_argument('-v','--vcf',metavar='File',dest='vcf',help='Tne path of VCF file',type=str,required=True)
parser.add_argument('-G','--GzFile',dest='GzFile',help='The input is gz file',action='store_true',default=False)
parser.add_argument('-S','--Sample',metavar='File',dest='Sample',help='Sample List file',type=str,required=True)
parser.add_argument('-O','--Outgroup',metavar='File',dest='Outgroup',help='Outgroup List file',type=str,required=True)
parser.add_argument('-i','--iterate',metavar='Ind',dest='iterate',help='The number of iterate(seed) (default:100)',type=int,default=100)
parser.add_argument('-o','--Output',metavar='File',dest='output',help='Output file',type=argparse.FileType('w'),required=True)
args=parser.parse_args()
###########################
if __name__=='__main__':
    main()