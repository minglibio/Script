# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Thu Jan 10 23:21:10 CST 2019
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadFa(file):
    Dict = {}
    seq = ''
    for line in file:
        line = line.strip()
        if line[0] == '>':
            if len(seq) > 0:
                Dict[name] = seq
            temp = line.split()
            name = temp[0][1:]
            seq = ''
        else:
            seq += line
    Dict[name] = seq
    return Dict
def ReverseComplement(Seq):
    return ''.join(["ATCGN"["TAGCN".index(n)] for n in Seq.upper()[::-1]])
@click.command()
@click.option('-f','--fasta',type=click.File('r'),help='The input file',required=True)
@click.option('-c','--chr',type=str,help='The chr need ReverseComplement. e.g. chr1,chr2,chr5',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(fasta,chr,output):
    Fa = LoadFa(fasta)
    ChrList = chr.split(',')
    for Chr in ChrList: Fa[Chr] = ReverseComplement(Fa[Chr])
    for key,value in Fa.items(): output.write(f'>{key}\n{value}\n')
if __name__ == '__main__':
    main()
