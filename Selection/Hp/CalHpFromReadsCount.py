# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Thu Feb 16 20:55:19 2017
@Mail: minnglee@163.com
@Author: Ming Li
"""

###用于非标准VCF文件

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadReadsCountCount(File):
    '''
    CHR     Pos     Ref     Alt
    1       87      1198    1091
    1       88      1216    1095
    '''
    Dict = {}
    ChrSet = set()
    next(File)
    for line in File:
        line = line.strip().split()
        if int(line[-1]) > int(line[-2]): line[-2],line[-1] = line[-1],line[-2]
        Dict.setdefault(line[0],[]).append([int(line[1]),int(line[-2]),int(line[-1])])
        ChrSet.add(line[0])
    return Dict,ChrSet
def SlideWindow(start,end,step,Index,InList):
    SubList = []
    for i in range(Index,len(InList)):
        if InList[i][0] <= start + step:
            SubList.append(InList[i])
            Index = i+1
        elif InList[i][0] <= end: SubList.append(InList[i])
        else: return SubList,Index,True
    return SubList,Index,False
def CalculateWindow(List):
    MaxAllele,MinAllele = 0,0
    SnpNum = len(List)
    if SnpNum == 0: return 0,0
    else:
        for i in List:
            MaxAllele += i[1]
            MinAllele += i[2]
        if MaxAllele == 0 : return 0,0
        else : Hp = 2*MaxAllele*MinAllele/(MaxAllele+MinAllele)**2
        return SnpNum,Hp
@click.command()
@click.option('-i','--input',help='Input file',type=click.File('r'),required=True)
@click.option('-w','--window',help='Slide Window Size',type=int,default=50000)
@click.option('-s','--step',help='Step Size',type=int,default=10000)
@click.option('-o','--output',help='Output file',type=click.File('w'),required=True)
def main(input,window,step,output):
    output.write('CHR\tSTART\tEND\tSnpNum\tHp\n')
    ReadsCountDict,ChrSet = LoadReadsCountCount(input)
    for CHR in ChrSet:
        start,end = 0,window
        Index = 0
        NotEnd = True
        while NotEnd :
            WinSnpList,Index,NotEnd = SlideWindow(start,end,step,Index,ReadsCountDict[CHR])
            SnpNum,Hp = CalculateWindow(WinSnpList)
            output.write(f'{CHR}\t{start}\t{end}\t{SnpNum}\t{Hp}\n')
            start += step
            end += step
if __name__ == '__main__':
    main()
