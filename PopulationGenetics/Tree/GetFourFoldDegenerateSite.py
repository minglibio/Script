# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Thu Jul 12 10:11:51 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click,re

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
def Codon():
    Dict = {'CG' : 'Arg',
            'CC' : 'Pro',
            'TC' : 'Ser',
            'CT' : 'Leu',
            'GT' : 'Val',
            'AC' : 'Thr',
            'GC' : 'Ala',
            'GG' : 'Gly'}
    return Dict
def ReverseComplement(Seq):
    return ''.join(["ATCGN"["TAGCN".index(n)] for n in Seq.upper()[::-1]])
@click.command()
@click.option('-g','--gtf',type=click.File('r'),help='The GTF file',required=True)
@click.option('-f','--fasta',type=click.File('r'),help='The fasta file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(gtf,fasta,output):
    FourFold = {}
    CodonDict = Codon()
    fasta = LoadFasta(fasta)
    for line in gtf:
        if line.startswith('#'): continue
        line = line.strip().split('\t')
        if line[2] == 'CDS':
            GeneName = re.search('(?<=gene=).*?(?=;)',line[8]).group()
            Chrom = line[0]
            Start = int(line[3]) - 1
            End = int(line[4]) - 1
            Strand = line[6]
            Frame = int(line[7])
        else: continue
        PosList = []
        if Strand == '+':
            seq = fasta[Chrom][Start:End+1].upper()
            for i in range(Start,End+1):
                PosList.append(i)
        elif Strand == '-':
            seq = ReverseComplement(fasta[Chrom][Start:End+1].upper())
            for i in range(End,Start-1,-1):
                PosList.append(i)
        i = Frame
        while i < len(seq)-2:
            if seq[i:i+2] in CodonDict:
                Index = f'{Chrom}-{PosList[i+2]+1}'
                FourFold[Index] = [GeneName,Strand]
            i += 3
    for key,value in FourFold.items():
        Pos = key.split('-') 
        output.write(f'{Pos[0]}\t{Pos[1]}\t{Pos[1]}\t{value[0]}\t{value[1]}\n')
if __name__ == '__main__':
    main()
