# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Tue Aug 14 20:10:00 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadIBD(file):
    '''
    26      64197   0.0013736263736263737   2
    26      64198   0.0013736263736263737   2
    26      64199   0.0013736263736263737   2
    '''
    List = []
    for line in file:
        line = line.strip().split()
#        List.append([int(line[1]),int(line[-1])])
        List.append([int(line[1]),float(line[2])])
    Chr = line[0]
    return List,Chr
def ReturnSlideWindowIndex(start,end,step,StartIndex,List):
    SubList = []
    try:
        for i in range(StartIndex,end):
            if List[i][0] <= start + step:
                SubList.append(List[i][1])
                StartIndex = i + 1
            elif List[i][0] <= end : SubList.append(List[i][1])
            else : break
        return SubList,StartIndex,True
    except IndexError:
        return SubList,StartIndex,False
def CalculateWindow(List,StartIndex):
    PosNum = len(List)
    if PosNum == 0:
        return 0,StartIndex
    else:
        TotalDepth = 0
        for i in List: TotalDepth += i
        return TotalDepth,StartIndex
@click.command()
@click.option('-i','--ibd',type=click.File('r'),help='The IBD depth file',required=True)
@click.option('-w','--window',type=int,help='The window size',default=10000)
@click.option('-s','--step',type=int,help='The step size',default=5000)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(ibd,window,step,output):
    output.write('CHR\tSTART\tEND\tTotalDepth\tMeanDepth\n')
    List,Chr = LoadIBD(ibd)
    print('IBD loaded!')
    end,start,StartIndex = window,0,0
    NotEnd = True
    while NotEnd :
        SubList,StartIndex,NotEnd = ReturnSlideWindowIndex(start,end,step,StartIndex,List)
        TotalDepth,StartIndex = CalculateWindow(SubList,StartIndex)
        output.write(f'{Chr}\t{start+1}\t{end+1}\t{TotalDepth}\t{TotalDepth/window}\n')
        start += step
        end += step
if __name__ == '__main__':
    main()
