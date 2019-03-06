# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Mon Aug 13 20:21:18 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadIndividual(file):
    Dict = {}
    for line in file: Dict[line.strip()] = None
    return Dict
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
@click.option('--keep',type=click.File('r'),help='The input file')
@click.option('--remove',type=click.File('r'),help='The input file')
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,keep,remove,output):
    Fasta = LoadFasta(input)
    if keep:
        Sample = LoadIndividual(keep)
        for sample,seq in Fasta.items():
            if sample not in Sample: continue
            output.write(f'>{sample}\n{seq}\n')
    if remove:
        Sample = LoadIndividual(remove)
        for sample,seq in Fasta.items():
            if sample in Sample: continue
            output.write(f'>{sample}\n{seq}\n')
if __name__ == '__main__':
    main()
