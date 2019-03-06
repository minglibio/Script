# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Wed Jul 18 15:09:49 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def HandleOutput(path):
    FileList = sorted(os.listdir(path))
    for file in FileList:
        FileName = file.split('.')[0]
        if not os.path.exists(f'{path}/{FileName}.o'): os.system(f'rm {path}/{file}')
        if not os.path.exists(f'{path}/{FileName}.e'): os.system(f'rm {path}/{file}')
@click.command()
@click.option('-p','--path',type=str,help='The path of bam file',required=True)
@click.option('-w','--bamlist',type=str,help='The list of bam file',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=4)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=5)
def main(path,bamlist,queue,corenum,memory):
    if path[-1] == '/' : path = path[:-1]
    if not os.path.exists(f'{path}/Check'): os.system(f'mkdir -p {path}/Check')
    output = f'{path}/Check'
    HandleOutput(output)
    #FileList = sorted(os.listdir(path))
    with open(bamlist,"r+") as FileList: 
        for file in FileList:
            file=file.strip()
            if file[-3:] != 'bam': continue
            FileName = os.path.basename(file).split(".")[0]
            if os.path.exists(f'{output}/{FileName}.o') : continue
            print(FileName)
            Command = f'samtools flagstat {file}'
            os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                         -q {queue} \
                         -n {corenum} \
                         -M {memory*1000000} \
                         -o {output}/{FileName}.o \
                         -e {output}/{FileName}.e \
                         -J {FileName}.check \
                         {Command}')
if __name__ == '__main__':
    main()
