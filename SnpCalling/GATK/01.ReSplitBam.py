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
    BamDict = {}
    for line in File:
        line = line.strip()
        Name = line.split('/')[-1].split('.')[0]
        BamDict[Name] = line
    return BamDict
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
#@click.option('-r','--region',type=click.File('r'),help='The region length file',required=True)
@click.option('-b','--bamlist',type=click.File('r'),help='The bamlist file',required=True)
#@click.option('-w','--window',type=int,help='The window size',default=20000000)
#@click.option('-o','--output',type=str,help='The output file',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=2)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=10)
@click.option('-p','--path',type=str,help='The path',required=True)
def main(bamlist,path,queue,corenum,memory):
    BamDict = LoadBam(bamlist)
    if path[-1] == '/' : path = path[:-1]
    List = os.popen(f'ls -hlF {path}').readlines()
    for line in List:
        line = line.strip()
        if not line[-1] == '/' : continue
        region = line.split()[-1][:-1]
        SubBamDict = {}
        SubBamList = os.popen(f"ls {path}/{region}/*.bam ").readlines()
        for bam in SubBamList :
            bam = bam.split('/')[-1].split('.')[0]
            SubBamDict[bam] = None
#            print(bam)
        for bam in BamDict.keys():
            if not bam in SubBamDict :
#                print(region,bam)
#                os.system(f'rm -f {path}/{region}/Shell/{bam}.sh')
#                os.system(f'rm -f {path}/{region}/Shell/{bam}.o')
#                os.system(f'rm -f {path}/{region}/Shell/{bam}.e')
                OUTPUT = open(f'{path}/{region}/Shell/{bam}.sh','w')
                OUTPUT.write(f'#/bin/bash\n')
                OUTPUT.write(f'samtools view -bS -h {BamDict[bam]} {region} > {path}/{region}/{bam}.{region}.bam\n')
                OUTPUT.write(f'samtools index {path}/{region}/{bam}.{region}.bam\n')
                os.system(f'chmod 755 {path}/{region}/Shell/{bam}.sh')
                print(f'bash {path}/{region}/Shell/{bam}.sh')
#                os.system(f'bash {path}/{region}/Shell/{bam}.sh')
'''
                os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                     -q {queue} \
                     -n {corenum} \
                     -M {memory*1000000} \
                     -o {path}/{region}/Shell/{bam}.o \
                     -e {path}/{region}/Shell/{bam}.e \
                     -J {bam}.{region} \
                     bash {path}/{region}/Shell/{bam}.sh')
'''
if __name__ == '__main__':
    main()
