# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Sat Aug  4 20:18:09 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import math

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadBam(File):
    BamList = []
    for line in File:
        line = line.strip()
        BamList.append(line)
    return BamList
def Submit(queue,corenum,memory,Output,JobName,ShellName):
    os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                     -q {queue} \
                     -n {corenum} \
                     -M {memory*1000000} \
                     -o {Output}/{ShellName}.o \
                     -e {Output}/{ShellName}.e \
                     -J {JobName} \
                     {Output}/{ShellName}.sh')
def RenewRegion(Region):
    Region = Region.replace(':','-').split('-')
    if int(Region[1]) <= 1000: Start = Region[1]
    else: Start = int(Region[1]) - 1000
    End = int(Region[2]) + 1000
    return f'{Region[0]}:{Start}-{End}'
def GetShell(queue,corenum,memory,output,Region,BamList):
    Path = f'{output}/{Region}'
    ShellPath = f'{output}/{Region}/Shell'
    if not os.path.exists(Path): os.system(f'mkdir {Path}')
    if not os.path.exists(ShellPath): os.system(f'mkdir {ShellPath}')
    NewRegion = RenewRegion(Region)
    for Bam in BamList:
        Bam = Bam.strip()
        Name = Bam.split('/')[-1].split('.')[0]
        OUTPUT = open(f'{ShellPath}/{Name}.sh','w')
        OUTPUT.write(f'#/bin/bash\n')
        OUTPUT.write(f'samtools view -bS -h {Bam} {NewRegion} > {Path}/{Name}.{Region}.bam\n')
        OUTPUT.write(f'samtools index {Path}/{Name}.{Region}.bam\n')
        os.system(f'chmod 755 {ShellPath}/{Name}.sh')
        Submit(queue,corenum,memory,ShellPath,f'{Name}.{Region}',Name)
@click.command()
@click.option('-r','--region',type=click.File('r'),help='The region length file',required=True)
@click.option('-b','--bamlist',type=click.File('r'),help='The bamlist file',required=True)
@click.option('-w','--window',type=int,help='The window size',default=2000000)
@click.option('-o','--output',type=str,help='The output file',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=2)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=10)
def main(region,bamlist,window,output,queue,corenum,memory):
    '''
    input file:
    1:200000001-220000000
    2:20000001-40000000
    4:20000001-40000000
    '''
    BamList = LoadBam(bamlist)
    if output[-1] == '/' : output = output[:-1]
    for line in region:
        line = line.strip()
        Chr = line.split(':')[0]
        Region = line.split(':')[1].split('-')
        SplitNum = int((int(Region[1]) - int(Region[0]) + 1) / window)
        for i in range(SplitNum-1):
            RegionName = f'{Chr}:{int(Region[0]) + i * window}-{int(Region[0]) + (i+1) * window -1}'
            GetShell(queue,corenum,memory,output,RegionName,BamList)
        
        RegionName = f'{Chr}:{int(Region[0]) + (SplitNum-1) * window}-{Region[1]}'
        GetShell(queue,corenum,memory,output,RegionName,BamList)
if __name__ == '__main__':
    main()
