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
@click.option('-v','--vcf',type=click.File('r'),help='The list of VCF file (.gz file)',required=True)
@click.option('-o','--output',type=str,help='The path of output file',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=20)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=105)
def main(vcf,output,queue,corenum,memory):
    if output[-1] == '/' : output = output[:-1]
    ShellPath = f'{output}/Shell'
    if not os.path.exists(ShellPath): os.system(f'mkdir {ShellPath}')
    for VCF in vcf:
        VCF = VCF.strip()
        Name = VCF.split('/')[-1].replace('.vcf.gz','')
        Chr = Name.split(':')[0].split('.')[1]
        ShellName = f'{ShellPath}/{Name}.sh'
        OUTPUT = open(ShellName,'w')
        OUTPUT.write(f'#!/bin/bash\n')
        OUTPUT.write(f'java -Xmx{memory}g -Xss128m -jar ~/software/beagle.27Jun16.b16.jar chrom={Chr} gt={VCF} out={Name}.phase gprobs=true nthreads={corenum}\n')
#        OUTPUT.write(f'java -Xmx{memory}g -Xss128m -jar ~/software/beagle.27Jun16.b16.jar chrom={Chr} gt={VCF} out={Name}.phase gprobs=true nthreads={corenum} ibdtrim=40 ibd=true ibdlod=1\n')
#        OUTPUT.write(f'java -Xmx{memory}g -Xss128m -jar ~/software/beagle.27Jun16.b16.jar chrom={Chr} gt={Name}.imp.vcf.gz out={Name}.imp.phase gprobs=true nthreads={corenum} lowmem=true\n')
        os.system(f'chmod 755 {ShellPath}/{Name}.sh')
#'''        ######## Submit
        os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                    -q {queue} \
                    -n {corenum} \
                    -M {memory*1000000} \
                    -o {ShellPath}/{Name}.o \
                    -e {ShellPath}/{Name}.e \
                    -J Phase.{Name} \
                    bash {ShellName}')
#'''
if __name__ == '__main__':
    main()
