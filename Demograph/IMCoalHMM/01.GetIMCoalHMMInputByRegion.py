# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Sat Aug  4 20:18:09 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import math

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def Submit(queue,corenum,memory,Output,ShellName,Command):
    os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                     -q {queue} \
                     -n {corenum} \
                     -M {memory*1000000} \
                     -o {Output}/shell/{ShellName}.o \
                     -e {Output}/shell/{ShellName}.e \
                     -J {ShellName} \
                     "{Command}"')
@click.command()
@click.option('--chr',type=click.File('r'),help='The chr length file',required=True)
@click.option('-v','--vcf',type=str,help='The vcf file',required=True)
@click.option('-r','--ref',type=str,help='The reference file',required=True)
@click.option('-s','--sample',type=str,help='The sample name',required=True)
@click.option('-w','--window',type=int,help='The window size',default=1000000)
#@click.option('-s','--step',type=int,help='The step size',default=10000000)
#@click.option('-o','--output',type=str,help='The output file path',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=1)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=5)
def main(chr,vcf,ref,sample,window,queue,corenum,memory):
    '''
    input file:
    1       275406953
    2       248966461
    '''
    output = sample
#    if output[-1] == '/' : output = output[:-1]
    if not os.path.exists(f'{output}'): os.system(f'mkdir {output}')
    if not os.path.exists(f'{output}/shell'): os.system(f'mkdir {output}/shell')
    for line in chr :
        line = line.strip().split()
        Chr = line[0]
        
        Num = math.floor(int(line[1])/window)
        Start,End = 1,window
        for i in range(1,Num + 1):
            if int(line[1]) - End <= window * 0.5:
                End = int(line[1])
                Region = f'{Chr}:{Start}-{End}'
                Name = f'{sample}.{Region}'
                Command = f'samtools faidx {ref} {Region} | bcftools consensus {vcf} -s {sample} -o {output}/{Name}.fa'
                Submit(queue,corenum,memory,output,Name,Command)
                continue
            Region = f'{Chr}:{Start}-{End}'
            Name = f'{sample}.{Region}'
            Command = f'samtools faidx {ref} {Region} | bcftools consensus {vcf} -s {sample} -o {output}/{Name}.fa'
            Submit(queue,corenum,memory,output,Name,Command)
            Start = 1 + window * i
            End = window * (i+1)
        if End != int(line[1]):
            End = int(line[1])
            Region = f'{Chr}:{Start}-{End}'
            Name = f'{sample}.{Region}'
            Command = f'samtools faidx {ref} {Region} | bcftools consensus {vcf} -s {sample} -o {output}/{Name}.fa'
            Submit(queue,corenum,memory,output,Name,Command)
if __name__ == '__main__':
    main()
