# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Tue Dec 12 15:01:40 2017
@Mail: minnglee@163.com
@Author: Ming Li
"""
import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadSweepFinder(file):
    '''
    1A	1363825.000000	0.028874
    1A	1363984.000000	0.383478
    1A	2977401.000000	0.071541
    '''
    Dict = {}
    ChrSet = set()
#    next(file)
    for line in file:
        line = line.strip().split()
        Chr,Position = line[0],float(line[1])
        Dict.setdefault(Chr,[]).append([Position,float(line[-1])])
        ChrSet.add(Chr)
    return Dict,ChrSet
def ReturnSlideWindowIndex(start,end,step,LastIndex,DictList):
    List=[]
    index=LastIndex
    try:
        for i in range(LastIndex,end):
            if DictList[i][0] <= start + step:
                List.append(DictList[i][1])
                index = i+1
            elif DictList[i][0] <= end: List.append(DictList[i][1])
            else: break
        return List,index,True
    except IndexError:
        return List,index,False
def CalculateWindow(List):
    SnpNum=len(List)
    if SnpNum == 0 : return 0,0
    else : return SnpNum,max(List)
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-w','--window',type=int,help='Slide Window Size',default=100000)
@click.option('-s','--step',type=int,help='Step Size',default=100000)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,window,step,output):
    output.write('CHR\tSTART\tEND\tSnpNum\tSweepFinder\n')
    SFDict,ChrSet = LoadSweepFinder(input)
    print('SweepFinder loaded!')
    for CHR in ChrSet:
        start,end = 0,window
        StartIndex = 0
        NotEnd = True
        while NotEnd :
            WinSnpList,StartIndex,NotEnd = ReturnSlideWindowIndex(start,end,step,StartIndex,SFDict[CHR])
            SnpNum,MaxSweepFinder = CalculateWindow(WinSnpList)
            output.write(f'{CHR}\t{start}\t{end}\t{MaxSweepFinder}\n')
            start += step
            end += step
if __name__ == '__main__':
    main()
