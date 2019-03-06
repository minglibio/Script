# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Wed Jul 26 15:34:36 2017
@Mail: minnglee@163.com
@Author: Ming Li
"""
#将Fst与π ln ratio的Z test 同时显著的窗口进一步合并

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadSignRegions(file):
    '''
    Chrom	Start (bp)	End (bp)	In Pi Ratio	Z(In Pi Ratio)	P
    1	21410001	21450000	2.287011929	8.992159889	0
    1	21420001	21460000	2.07362382	8.132256243	0
    '''
    Dict = {}
    for line in file:
        if line.startswith("Chrom"): continue
        if line.startswith("Chr"): continue
        line = line.strip().split()
        Dict.setdefault(line[0],[]).append([int(line[1]),int(line[2])])
    return Dict
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-d','--distance',type=int,help='The max distance that two window merged[1]',default=1)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,distance,output):
    SignRegions = LoadSignRegions(input)
    for key,value in SignRegions.items():
        RegionList = sorted(value, key=lambda x : x[0])
        start = RegionList[0][0]
        end = RegionList[0][1]
        for region in RegionList:
            if region[0] - end > distance + 1:
                output.write(f'{key}\t{start}\t{end}\t{end-start}\n')
                start,end = region[0],region[1]
            else:
                end = region[1]
        output.write(f'{key}\t{start}\t{end}\t{end-start}\n')
if __name__ == '__main__':
    main()
