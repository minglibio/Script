# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Thu Jul 19 10:44:44 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-i','--input',type=click.File('r'),help='The list of input file',required=True)
@click.option('-o','--output',type=str,help='The output path',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=4)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=10)
def main(input,output,queue,corenum,memory):
    if output[-1] == '/': output = output[:-1]
    ScriptDir = f'{output}/shell'
    if not os.path.exists(f'{ScriptDir}'): os.system(f'mkdir -p {ScriptDir}')
    for line in input:
        line = line.strip()
        Name = os.path.basename(line)
        Dir = os.path.dirname(line)
#        print(Name,Dir)
        PreName = Name.replace('.sra','')
#        print(PreName)
        OUTPUT = open(f'{ScriptDir}/{PreName}.sh','w')
        OUTPUT.write('#!/bin/bash\n')
        OUTPUT.write(f'fastq-dump --gzip --split-3 {line} -O {output}\n')
        OUTPUT.write(f'mv {output}/{PreName}_1.fastq.gz {output}/{PreName}.R1.fq.gz\n')
        OUTPUT.write(f'mv {output}/{PreName}_2.fastq.gz {output}/{PreName}.R2.fq.gz\n')
#        OUTPUT.write(f'gzip {output}/{PreName}.R1.fq\n')
#        OUTPUT.write(f'gzip {output}/{PreName}.R2.fq\n')
        os.system(f'chmod 755 {ScriptDir}/{PreName}.sh')
        os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                         -q {queue} \
                         -n {corenum} \
                         -M {memory*1000000} \
                         -o {output}/{PreName}.o \
                         -e {output}/{PreName}.e \
                         -J {PreName}.S2F \
                         {ScriptDir}/{PreName}.sh')
if __name__ == '__main__':
    main()
