# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Mon Sep 18 16:14:07 2017
@Mail: minnglee@163.com
@Author: Ming Li
"""
# 将 VCF 每个个体分成两个 haplotype 输出为 fasta 格式
import sys,os,logging,click,re

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-v','--vcf',type=str,help='The VCF file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(vcf,output):
    SeqDict = {}
    VCFFile = os.popen(f'less {vcf}').readlines()
    for line in VCFFile:
        if line.startswith('##'): continue
        line = line.strip().split()
        if line[0] == '#CHROM':
            SampleList = line[9:]
            RowNum = len(line)
        else:
            Allele = {'0':line[3],'1':line[4]}
            for i in range(9,RowNum):
                GT = line[i].split(':')[0].split('|')
                SeqDict.setdefault(i*2,[]).append(Allele[GT[0]])
                SeqDict.setdefault(i*2+1,[]).append(Allele[GT[1]])
    for key,value in SeqDict.items():
        seq = ''.join(value)
        Hap = key%2+1
        Sample = key//2 - 9
        output.write(f'>{SampleList[Sample]}_{Hap}\n{seq}\n')
if __name__ == '__main__':
    main()
