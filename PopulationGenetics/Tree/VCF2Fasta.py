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
@click.option('-v','--vcf',type=str,help='The VCF file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(vcf,output):
    DegenerateDict = Degenerate()
    SeqDict = {}
    VCFFile = os.popen(f'less {vcf}').readlines()
    for line in VCFFile:
        if line.startswith('##'): continue
        line = line.strip().split()
        if line[0] == '#CHROM':
            SampleList = line[9:]
            RowNum = len(line)
        else:
            Ref,Alt = line[3],line[4]
            RefAlt = f'{line[3]}{line[4]}'
            for i in range(9,RowNum):
                GT = line[i].split(':')[0]
                if GT == '0/0' or GT == '0|0':
                    SeqDict.setdefault(i,[]).append(Ref)
                elif GT == '0/1' or GT == '0|1' or GT == '1|0':
                    SeqDict.setdefault(i,[]).append(DegenerateDict[RefAlt])
                elif GT == '1/1' or GT == '1|1':
                    SeqDict.setdefault(i,[]).append(Alt)
                else:
                    SeqDict.setdefault(i,[]).append('N')
    for key,value in SeqDict.items():
        seq = ''.join(value)
        output.write(f'>{SampleList[key-9]}\n{seq}\n')
if __name__ == '__main__':
    main()
