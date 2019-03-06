# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Mon Jul  9 09:39:08 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''
# The format of input file must like: XXX.R1.fq.gz or XXX.R1.clean.fq.gz. If not, you can run 01.ChangeFastqFileNameInDir.py

import sys,os,logging,click,re

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-p','--path',type=str,help='The error file path',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='mem128queue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=16)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=180)
def main(path,queue,corenum,memory):
    if path[-1] == '/': path = path[:-1]
    OutDir = f'{path}/ReSubmit'
    if not os.path.exists(f'{OutDir}'): os.system(f'mkdir -p {OutDir}')
    FileList = sorted(os.listdir(f'{path}/shell'))
    for File in FileList:
        if not File.endswith('.e'):continue
        FileName = File.split('.')[0]
        NeedReSubmit = True
        ErrorFile = open(f'{path}/shell/{FileName}.e','r')
        for line in ErrorFile:
            line = line.strip()
            if re.search('picard.sam.markduplicates.MarkDuplicates done',line): NeedReSubmit = False
        if NeedReSubmit:
            print(File)
            os.system(f'mv {path}/shell/{FileName}.e {path}/shell/{FileName}.e.resubmit')
            Input = open(f'{path}/shell/{FileName}.mapping.sh','r')
            Output = open(f'{OutDir}/{FileName}.dedup.sh','w')
            Output.write('#!/bin/bash\n')
            for line in Input:
                line = line.strip()
                if re.search('MarkDuplicates',line): 
                    line = re.sub('-Xmx.*g',f'-Xmx{memory}g',line)
                    Output.write(f'{line}\n')
            Output.write(f'echo {FileName} remove dup finished!\n')
            os.system(f'chmod 755 {OutDir}/{FileName}.dedup.sh')
#''' 
            os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                     -q {queue} \
                     -n {corenum} \
                     -M {memory*1000000} \
                     -o {OutDir}/{FileName}.o \
                     -e {OutDir}/{FileName}.e \
                     -J {FileName}.dedup \
                     {OutDir}/{FileName}.dedup.sh')
#'''
if __name__ == '__main__':
    main()
