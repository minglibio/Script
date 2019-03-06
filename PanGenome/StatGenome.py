# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Wed Oct 17 16:11:15 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import numpy as np

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadFasta(File):
    Dict = {}
    seq = ''
    for line in File:
        line = line.strip()
        if line[0] == '>':
            if len(seq) > 0:
                Dict[name] = seq
            name = line.split()[0][1:]
            seq = ''
        else: seq += line
    Dict[name] = seq
    return Dict
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,output):
    FaDict = LoadFasta(input)
    LenList = []
    TotalBase = 0
    Gap = 0
    GC = 0
    for key,value in FaDict.items():
        LenList.append(len(value))
        TotalBase += len(value)
        Gap += value.upper().count('N')
        GC += value.upper().count('G')
        GC += value.upper().count('C')
    LenList.sort(reverse=True)
    Tmp = 0
    for scaffold in LenList:
        Tmp += scaffold
        if Tmp >= TotalBase * 0.5 :
            N50 = scaffold
            break
    output.write(f'Total sequence length:\t{TotalBase}\n')
    output.write(f'Total assembly gap length:\t{Gap}\n')
    output.write(f'GC ratio:\t{round(GC/(TotalBase-Gap),4)}\n')
    output.write(f'Number of scaffolds:\t{len(LenList)}\n')
    output.write(f'Scaffold N50:\t{N50}\n')
    output.write(f'Max Scaffold:\t{max(LenList)}\n')
    output.write(f'Min Scaffold:\t{min(LenList)}\n')
    output.write(f'Scaffold mean:\t{np.mean(LenList)}\n')
if __name__ == '__main__':
    main()
