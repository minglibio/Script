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

def LoadSample(file):
    Dict = {}
    for line in file:
        line = line.strip()
        Dict[line] = None
    return Dict
@click.command()
@click.option('-1','--sample1',type=click.File('r'),help='The sample 1 file',required=True)
@click.option('-2','--sample2',type=click.File('r'),help='The sample 2 file',required=True)
@click.option('-i','--ibd',type=click.File('r'),help='The IBD file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(sample1,sample2,ibd,output):
    '''
    IBD file:
    AOOA-AWD01      1       AOOA-AWD02      1       9       49780   71300   1.09
    AOOA-AWD01      1       AOOA-AWD02      1       9       127139  138678  1
    AOOA-AWD01      1       AOOA-AWD02      1       9       558634  567859  2.2
    '''
    Sample1 = LoadSample(sample1)
    Sample2 = LoadSample(sample2)
    All = len(Sample1) * len(Sample2) * 4
    DepthDict = {}
    for line in ibd:
        line = line.strip().split()
        if line[0] in Sample1 and line[2] in Sample2: pass
        elif line[0] in Sample2 and line[2] in Sample1: pass
        else: continue
        for i in range(int(line[5]),int(line[6])+1):
            DepthDict[i] = DepthDict.setdefault(i,0) + 1
    PosList = sorted(DepthDict.keys())
    for pos in PosList:
        output.write(f'{line[4]}\t{pos}\t{DepthDict[pos]/All}\t{DepthDict[pos]}\n')
if __name__ == '__main__':
    main()
