# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Mon Sep 18 16:14:07 2017
@Mail: minnglee@163.com
@Author: Ming Li
"""

import sys,os,logging,click,re

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def Degenerate():
    Dict = {'AG':'R',
            'GA':'R',
            'CT':'Y',
            'TC':'Y',
            'AC':'M',
            'CA':'M',
            'GT':'K',
            'TG':'K',
            'GC':'S',
            'CG':'S',
            'AT':'W',
            'TA':'W'}
    return Dict
@click.command()
@click.option('-i','--input',type=str,help='The VCF file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,output):
    DegenerateDict = Degenerate()
    SeqList = []
    Name = input.replace('.vcf','')
    Input = open(input)
    for line in Input:
        line = line.strip().split()
        Ref,Alt = line[0],line[1]
        RefAlt = f'{line[0]}{line[1]}'
        GT = line[2]
        if GT == '0/0' or GT == '0|0':
            SeqList.append(Ref)
        elif GT == '0/1' or GT == '0|1' or GT == '1|0':
            SeqList.append(DegenerateDict[RefAlt])
        elif GT == '1/1' or GT == '1|1':
            SeqList.append(Alt)
        else:
            SeqList.append('N')
    seq = ''.join(SeqList)
    output.write(f'>{Name}\n{seq}\n')
if __name__ == '__main__':
    main()
