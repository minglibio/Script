# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Sat Aug 11 14:49:05 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
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
@click.option('-f','--fasta',type=click.File('r'),help='The fasta file',required=True)
@click.option('-b','--bed',type=click.File('r'),help='The bed file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(fasta,bed,output):
    fasta = LoadFasta(fasta)
    for line in bed:
        line = line.strip().split()
        fasta[line[0]] = fasta[line[0]][:int(line[1])-1] + 'N'*(int(line[2])-int(line[1])+1) + fasta[line[0]][int(line[2]):]
    for chr,seq in fasta.items():
        output.write(f'>{chr}\n{seq}\n')
if __name__ == '__main__':
    main()
