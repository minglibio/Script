# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Wed Aug 22 17:26:07 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-b','--bed',type=click.File('r'),help='The bed file',required=True)
@click.option('-v','--vcf',type=str,help='The vcf file [gz]',required=True)
@click.option('-r','--root',type=str,help='The root of tree',default='Outgroup')
@click.option('-o','--output',type=str,help='The output file',default='.')
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='mem128queue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=1)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=10)
def main(bed,vcf,root,output,queue,corenum,memory):
    '''
    2       18545001        18560001        15000
    2       63245001        63250001        5000
    '''
    for line in bed:
        line = line.strip().split()
        Name = '-'.join(line[:3])
        if not os.path.exists(f'{output}/{Name}'): os.system(f'mkdir {output}/{Name}')
        Shell = open(f'{output}/{Name}/{Name}.sh','w')
        Shell.write('#/bin/bash\n')
        Shell.write(f'bcftools view {vcf} {line[0]}:{line[1]}-{line[2]} > {output}/{Name}/{Name}.vcf\n')
        Shell.write(f'gzip {output}/{Name}/{Name}.vcf\n')
        Shell.write(f'python3 ~/script/EvolutionTree/VCF2Fasta.py -v {output}/{Name}/{Name}.vcf.gz -o {output}/{Name}/{Name}.fa\n')
        Shell.write(f'bash ~/script/EvolutionTree/iqtree.sh {output}/{Name}/{Name}.fa {root} {corenum} {output}/{Name}/{Name}\n')
        os.system(f'chmod 755 {output}/{Name}/{Name}.sh')
###### submit
#'''
        os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                     -q {queue} \
                     -n {corenum} \
                     -M {memory*1000000} \
                     -o {output}/{Name}/{Name}.o \
                     -e {output}/{Name}/{Name}.e \
                     -J {Name}.tree \
                     {output}/{Name}/{Name}.sh')
#'''
if __name__ == '__main__':
    main()
