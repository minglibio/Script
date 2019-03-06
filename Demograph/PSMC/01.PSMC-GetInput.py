# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Tue Sep 25 19:59:32 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-b','--bam',type=click.File('r'),help='The file of bam list',required=True)
@click.option('--region',type=str,help='The file of region',required=True)
@click.option('--ref',type=str,help='The reference',required=True)
@click.option('-o','--output',type=str,help='The output file',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=2)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=10)
def main(bam,region,ref,output,queue,corenum,memory):
    if output[-1] == '/' : output = output[:-1]
    for line in bam:
        line = line.strip()
        Name = line.split('/')[-1].split('.')[0]
        if not os.path.exists(f'{output}/{Name}'): os.system(f'mkdir {output}/{Name}')
        if not os.path.exists(f'{output}/{Name}/shell'): os.system(f'mkdir {output}/{Name}/shell')
        OUTPUT = open(f'{output}/{Name}/shell/{Name}.sh','w')
        OUTPUT.write('#/bin/bash\n')
        OUTPUT.write(f'samtools mpileup -C 50 -q 20 -uf {ref} -l {region} {line} | bcftools call -c - | vcfutils.pl vcf2fq -d 3 -D 100 | gzip > {output}/{Name}/{Name}.diploid.fq.gz\n')
        OUTPUT.write(f'fq2psmcfa -q20 {output}/{Name}/{Name}.diploid.fq.gz > {output}/{Name}/{Name}.diploid.psmcfa\n')
        OUTPUT.write(f'/stor9000/apps/appsoftware/BioSoftware/software/psmc-master/utils/splitfa {output}/{Name}/{Name}.diploid.psmcfa > {output}/{Name}/{Name}.diploid.split.fa\n')
        os.system(f'chmod 755 {output}/{Name}/shell/{Name}.sh')
#'''
    ###### submit
        os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                     -q {queue} \
                     -n {corenum} \
                     -M {memory*1000000} \
                     -o {output}/{Name}/shell/{Name}.o \
                     -e {output}/{Name}/shell/{Name}.e \
                     -J PSMC.{Name} \
                     {output}/{Name}/shell/{Name}.sh')
#'''
if __name__ == '__main__':
    main()
