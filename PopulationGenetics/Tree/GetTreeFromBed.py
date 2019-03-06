# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Sun Sep  9 13:43:28 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-b','--bed',type=click.File('r'),help='The bed file',required=True)
@click.option('-v','--vcf',type=str,help='The vcf file',required=True)
@click.option('--outgroup',type=str,help='The name of outgroup',default='outgroup')
@click.option('-o','--output',type=str,help='The output file',default='.')
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=4)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=20)
def main(bed,vcf,outgroup,output,queue,corenum,memory):
    if output[-1] == '/': output = output[:-1]
    if not os.path.exists(f'{output}/shell'): os.system(f'mkdir {output}/shell')
    for line in bed:
        line = line.strip().split()
        Chr = line[0]
        Region = f'{Chr}:{line[1]}-{line[2]}'
        if os.path.exists(f'{output}/shell/{Region}.sh') : continue
     
        OUTPUT = open(f'{output}/shell/{Region}.sh','w')
        OUTPUT.write('#/bin/bash\n')
        OUTPUT.write(f'bcftools view {vcf} -r {Region} -O z -o {Region}.vcf.gz\n')
        OUTPUT.write(f'python3 ~/script/PopulationGenetics/Tree/VCF2HapFasta.py -v {Region}.vcf.gz -o {Region}.fa\n')
        OUTPUT.write(f'bash ~/script/PopulationGenetics/Tree/iqtree.sh {Region}.fa {outgroup} {corenum} {Region}\n')
        os.system(f'chmod 755 {output}/shell/{Region}.sh')
    ###### submit
#'''
        os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                     -q {queue} \
                     -n {corenum} \
                     -M {memory*1000000} \
                     -o {output}/shell/{Region}.o \
                     -e {output}/shell/{Region}.e \
                     -J Tree.{Region} \
                     {output}/shell/{Region}.sh')
#'''
if __name__ == '__main__':
    main()
