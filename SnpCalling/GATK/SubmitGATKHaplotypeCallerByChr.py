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

def Submit(queue,corenum,memory,output,region,outprefix,ref,sample):
    print(f'jsub -R "rusage[res=1]span[hosts=1]" \
            -q {queue} \
            -n {corenum} \
            -M {memory*1000000} \
            -o {output}/Shell/Sheep.{outprefix}.o \
            -e {output}/Shell/Sheep.{outprefix}.e \
            -J Sheep.GATK.{outprefix} \
            bash ~/script/SnpCalling/GATK.HaplotypeCaller.sh {region} {outprefix} {ref} {sample} {corenum}')
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-w','--window',type=int,help='The window size',default=20000000)
@click.option('-r','--ref',type=str,help='The reference genome',required=True)
@click.option('-s','--sample',type=str,help='The sample list file (XX.list)',required=True)
@click.option('-o','--output',type=str,help='The path of output file',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=20)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=100)
def main(input,window,ref,sample,output,queue,corenum,memory):
    '''
    input file:
    1       275406953
    2       248966461
    3       223996068
    '''
    if output[-1] == '/' : output = output[:-1]
    if not os.path.exists(f'{output}/Shell'): os.system(f'mkdir {output}/Shell')
    if not os.path.exists(f'{output}/Region'): os.system(f'mkdir {output}/Region')
    for line in input:
        line = line.strip().split()
        Chr = line[0]
        if int(line[1]) <= window + 2000000: Submit(queue,corenum,memory,output,Chr,Chr,ref,sample)
        else:
            Num = math.floor(int(line[1])/window)
            for i in range(Num):
                Start = 1 + window * i
                End = window * (i+1)
                Region = f'{output}/Region/{Chr}-{Start}-{End}.list'
                os.system(f'echo "{Chr}:{Start}-{End}" > {Region}')
                Submit(queue,corenum,memory,output,Region,f'{Chr}-{Start}-{End}',ref,sample)
            Start = 1 + window * Num
            End = line[1]
            Region = f'{output}/Region/{Chr}-{Start}-{End}.list'
            os.system(f'echo "{Chr}:{Start}-{End}" > {Region}')
            Submit(queue,corenum,memory,output,Region,f'{Chr}-{Start}-{End}',ref,sample)
if __name__ == '__main__':
    main()
