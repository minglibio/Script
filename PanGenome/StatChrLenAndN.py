# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Sat Aug 11 14:49:05 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import re
logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadFasta(File):
    Dict = {}
    seq = ''
    for line in File:
        line = line.strip()
        if line[0] == '>':
            if len(seq) > 0: Dict[name] = seq
            name = line.split()[0][1:]
            seq = ''
        else: seq += line
    Dict[name] = seq
    return Dict
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The fasta file',required=True)
@click.option('-o','--output',type=str,help='The prefix of output file',required=True)
def main(input,output):
    '''bed 格式 [start end) 0 based'''
    Fasta = LoadFasta(input)
    GenomeDict = open(f'{output}.bed','w')
    NDict = open(f'{output}.N.bed','w')
    for Chr,Seq in Fasta.items():
        GenomeDict.write(f'{Chr}\t0\t{len(Seq)}\n')
        NList = [[m.start(0), m.end(0)] for m in re.finditer('N+', Seq)]
        for N in NList :
            NDict.write(f'{Chr}\t{N[0]}\t{N[1]}\t{N[1]-N[0]}\n')
if __name__ == '__main__':
    main()
