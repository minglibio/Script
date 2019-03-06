# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Wed Aug 22 16:03:13 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadSignRegions(file,column,window,threshold):
    Dict = {}
    for line in file:
        if line.startswith("Chrom") or line.startswith("CHROM") or line.startswith("Chr") or line.startswith("CHR") or line.startswith("chr"): continue
        line = line.strip().split()
        if float(line[column-1]) < threshold: continue
        Dict.setdefault(line[0],[]).append([int(line[1]),int(line[1]) + window,float(line[column-1])])
    return Dict
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-t','--threshold',type=float,help='threshold',default=0)
@click.option('-k','--column',type=int,help='The column of data',default=3)
@click.option('-w','--window',type=int,help='The window size',default=1000)
@click.option('-g','--gap',type=int,help='The max gap between two windows which should be merge',default=50000)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,threshold,column,window,gap,output):
    SignRegions = LoadSignRegions(input,column,window,threshold)
    for key,value in SignRegions.items():
        RegionList = sorted(value, key=lambda x : x[0])
        start = RegionList[0][0]
        end = RegionList[0][1]
        for region in RegionList:
            if region[0] - end > gap + 1:
                output.write(f'{key}\t{start}\t{end}\t{end-start}\n')
                start,end = region[0],region[1]
            else:
                end = region[1]
        output.write(f'{key}\t{start}\t{end}\t{end-start}\n')
if __name__ == '__main__':
    main()
