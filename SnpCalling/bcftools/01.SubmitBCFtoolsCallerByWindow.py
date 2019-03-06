# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Sun Jul 29 00:44:31 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import math

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def Submit(queue,corenum,memory,ShellPath,Prefix,Region,ShellName):
    os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
            -q {queue} \
            -n {corenum} \
            -M {memory*1000000} \
            -o {ShellPath}/{Prefix}.{Region}.o \
            -e {ShellPath}/{Prefix}.{Region}.e \
            -J BCFtools.{Prefix}.{Region} \
            bash {ShellName}')
def GetShell(corenum,ShellPath,Prefix,SampleList,Ref,Chr,Start,End):
    Region = f'{Chr}:{Start}-{End}'
    ShellName = f'{ShellPath}/{Prefix}.{Region}.sh'
    OUTPUT = open(ShellName,'w')
    OUTPUT.write(f'#!/bin/bash\n')
    OUTPUT.write(f'bcftools mpileup -b {SampleList} -C 50 -d 250 -f {Ref} -q 20 -Q 20 -r {Region} -a FORMAT/DP,AD --threads {corenum} -O b -o {Prefix}.{Region}.bcf.gz\n')
    OUTPUT.write(f'bcftools call -V indels -O z -o {Prefix}.{Region}.vcf.gz {Prefix}.{Region}.bcf.gz -m -v\n')
    os.system(f'chmod 755 {ShellName}')
    return Region,ShellName
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-w','--window',type=int,help='The window size',default=10000000)
@click.option('-l','--length',type=int,help='The length',default=1000000)
@click.option('-r','--ref',type=str,help='The reference genome',required=True)
@click.option('-s','--sample',type=str,help='The sample list file (XX.list)',required=True)
@click.option('-o','--output',type=str,help='The path of output file',required=True)
@click.option('-p','--prefix',type=str,help='The prefix of output file',default='BCFtools')
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=4)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=20)
def main(input,window,length,ref,sample,output,prefix,queue,corenum,memory):
    '''
    input file:
    1       275406953
    2       248966461
    3       223996068
    '''
    if output[-1] == '/' : output = output[:-1]
    ShellPath = f'{output}/Shell'
    if not os.path.exists(ShellPath): os.system(f'mkdir {ShellPath}')
    for line in input:
        line = line.strip().split()
        Chr = line[0]
        if int(line[1]) <= window + length:
            Start,End = 1,int(line[1])
            Region,ShellName = GetShell(corenum,ShellPath,prefix,sample,ref,Chr,Start,End)
            Submit(queue,corenum,memory,ShellPath,prefix,Region,ShellName)
        else:
            Num = math.floor(int(line[1])/window)
            for i in range(Num):
                Start = 1 + window * i
                End = window * (i+1)
                Region,ShellName = GetShell(corenum,ShellPath,prefix,sample,ref,Chr,Start,End)
                Submit(queue,corenum,memory,ShellPath,prefix,Region,ShellName)
            Start = 1 + window * Num
            End = line[1]
            Region,ShellName = GetShell(corenum,ShellPath,prefix,sample,ref,Chr,Start,End)
            Submit(queue,corenum,memory,ShellPath,prefix,Region,ShellName)
if __name__ == '__main__':
    main()
