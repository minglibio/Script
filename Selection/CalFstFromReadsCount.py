# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Thu Mar  1 20:27:57 2018
@Mail: minnglee@163.com
@Author: Ming Li
"""

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadSample(File):
    Dict = {}
    for line in File:
        line = line.strip()
        Dict[line] = None
    return Dict
def CalNandD(ReadsCountList,Pop1,Pop2,maf):
    a1,n1,a2,n2 = 0,0,0,0
    for i in Pop1:
        ReadsCount = ReadsCountList[i].split('/')
        a1 += int(ReadsCount[0])
        n1 += (int(ReadsCount[0]) + int(ReadsCount[1]))
    for i in Pop2:
        ReadsCount = ReadsCountList[i].split('/')
        a2 += int(ReadsCount[0])
        n2 += (int(ReadsCount[0]) + int(ReadsCount[1]))
    if n1 < 2 or n2 < 2:
        return 0,0,False
    elif (a1+a2)/(n1+n2) < maf or (a1+a2)/(n1+n2) > 1 - maf or n1+n2 < 300: 
        return 0,0,False
    else:
        h1 = (a1*(n1-a1))/(n1*(n1-1))
        h2 = (a2*(n2-a2))/(n2*(n2-1))
        N = (a1/n1 - a2/n2)**2 - h1/n1 -h2/n2
        D = N + h1 + h2
        return N,D,True
def LoadGT(File,POP1,POP2,maf):
    '''
    Chr     Pos     Ref     Alt     SG-1    SG-2    SG-3    SG-4    SG-5    SG-6    SG-7    SG-8
    1       4508    T       C       9/2/0   6/3/0   6/1/0   11/1/0  4/1/0   2/4/0   11/1/0  7/1/0
    1       4520    A       T       0/11/0  0/9/0   0/9/0   0/14/0  0/6/0   0/6/0   0/14/0  0/10/0
    '''
    Dict = {}
    Chr = set()
    Pop1Index = []
    Pop2Index = []
    Pop1Dict = LoadSample(POP1)
    Pop2Dict = LoadSample(POP2)
    for line in File:
        line = line.strip().split()
        if line[0] == 'Chr':
            for i in range(4,len(line)):
                if line[i] in Pop1Dict: Pop1Index.append(i)
                elif line[i] in Pop2Dict: Pop2Index.append(i)
            continue
        N,D,SNP = CalNandD(line,Pop1Index,Pop2Index,maf)
        if SNP:
            Chr.add(line[0])
            Dict.setdefault(line[0],[]).append([int(line[1]),N,D])
    return Dict,Chr
def ReturnSlideWindowIndex(start,end,step,LastIndex,DictList):
    List = []
    index = LastIndex
    try:
        for i in range(LastIndex,end):
            if DictList[i][0] <= start + step:
                List.append(DictList[i][1:3])
                index = i+1
            elif DictList[i][0] <= end:
                List.append(DictList[i][1:3])
            else:
                break
        return List,index,True
    except IndexError:
        return List,index,False
def CalculateWindow(List,StartIndex):
    SnpNum=len(List)
    if SnpNum == 0:
        if StartIndex != 0:
            StartIndex -= 1
        return 0,0,StartIndex
    else:
        SumN,SumD = 0,0
        for i in List:
            SumN += i[0]
            SumD += i[1]
        if SumD == 0: F = 0
        else: F = SumN/SumD
        return SnpNum,F,StartIndex
@click.command()
@click.option('-i','--input',help='Input file',type=click.File('r'),required=True)
@click.option('-1','--pop1',help='Pop 1 List file',type=open,required=True)
@click.option('-2','--pop2',help='Pop 2 List file',type=open,required=True)
@click.option('-w','--window',help='Slide Window Size',type=int,default=50000)
@click.option('-s','--step',help='Step Size',type=int,default=10000)
@click.option('-m','--maf',help='MAF',type=float,default=0.05)
@click.option('-o','--output',help='Output file',type=click.File('w'),required=True)
def main(input,pop1,pop2,window,step,maf,output):
    output.write('CHR\tSTART\tEND\tSnpNum\tFst\n')
    FstDict,ChrSet = LoadGT(input,pop1,pop2,maf)
    logging.info('Genotype loaded!')
    for CHR in ChrSet:
        end = window
        start = 0
        StartIndex = 0
        NotEnd = True
        while NotEnd :
            WinSnpList,StartIndex,NotEnd = ReturnSlideWindowIndex(start,end,step,StartIndex,FstDict[CHR])
            SnpNum,WinFst,StartIndex = CalculateWindow(WinSnpList,StartIndex)
            output.write(f'{CHR}\t{start}\t{end}\t{SnpNum}\t{WinFst}\n')
            start += step
            end += step
if __name__ == '__main__':
    main()
