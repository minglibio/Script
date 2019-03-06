# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Fri Sep 28 15:42:53 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-i','--input',type=str,help='The input VCF file',required=True)
@click.option('-o','--output',type=str,help='The output file',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=2)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=10)
def main(input,output,queue,corenum,memory):
    if output[-1] == '/' : output = output[:-1]
    if not os.path.exists(f'{output}/shell'): os.system(f'mkdir {output}/shell')
    SampleList = os.popen(f'bcftools query -l {input}').readlines()
    for sample in SampleList:
        sample = sample.strip()
        print(sample)
        OUTPUT = open(f'{output}/shell/{sample}.sh','w')
        OUTPUT.write('#/bin/bash\n')
        OUTPUT.write(f"bcftools query -s {sample} -f '%REF\\t%ALT\\t[%GT]\\n' {input}|grep -v ^X > {sample}.vcf\n")
        OUTPUT.write(f'python3 ~/script/PopulationGenetics/Tree/rapidNJ/VCF2Fasta.py -i {sample}.vcf -o {sample}.fa\n')
        os.system(f'chmod 755 {output}/shell/{sample}.sh')
#'''
    ###### submit
        os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                     -q {queue} \
                     -n {corenum} \
                     -M {memory*1000000} \
                     -o {output}/shell/{sample}.o \
                     -e {output}/shell/{sample}.e \
                     -J {sample} \
                     bash {output}/shell/{sample}.sh')
#'''
if __name__ == '__main__':
    main()
