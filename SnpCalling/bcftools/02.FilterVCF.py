# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Sun Jul 29 00:44:31 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-p','--path',type=str,help='The path of VCF file (.gz file)',required=True)
@click.option('-d','--depth',type=int,help='The mean depth of BAM file',default=10)
@click.option('-o','--output',type=str,help='The path of output file',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=2)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=15)
def main(path,depth,output,queue,corenum,memory):
    if path[-1] == '/' : path = path[:-1]
    if output[-1] == '/' : output = output[:-1]
    ShellPath = f'{output}/Shell'
    if not os.path.exists(ShellPath): os.system(f'mkdir {ShellPath}')
    VCFList = os.popen(f'ls  {path}/*.vcf.gz').readlines()
    for VCF in VCFList:
        VCF = VCF.strip()
        Name = VCF.split('/')[-1].replace('.vcf.gz','')
        ShellName = f'{ShellPath}/{Name}.sh'
        OUTPUT = open(ShellName,'w')
        OUTPUT.write(f'#!/bin/bash\n')
        OUTPUT.write(f'vcftools --gzvcf {VCF} --minQ 30 --min-alleles 2 --max-alleles 2 --min-meanDP {round(depth/3,2)} --max-meanDP {depth*3} --max-missing 0.9 --non-ref-ac 2 --remove-indels --recode --recode-INFO-all --out {output}/{Name}.flt\n')
        OUTPUT.write(f'gzip {output}/{Name}.flt.recode.vcf')
        ######## Submit
        os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                    -q {queue} \
                    -n {corenum} \
                    -M {memory*1000000} \
                    -o {ShellPath}/{Name}.o \
                    -e {ShellPath}/{Name}.e \
                    -J VCFFilter.{Name} \
                    bash {ShellName}')
if __name__ == '__main__':
    main()
