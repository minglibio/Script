# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Mon Jul  9 09:39:08 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''
# The format of input file must like: XXX.R1.fq.gz or XXX.R1.clean.fq.gz. If not, you can run 01.ChangeFastqFileNameInDir.py

import sys,os,logging,click,re

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

Picard = 'java -Xmx20g -Djava.io.tmpdir=/stor9000/apps/users/NWSUAF/2015050469/tmp -jar /stor9000/apps/users/NWSUAF/2015050469/software/picard-2.18.7.jar'
def AddOrReplaceReadGroups(InBam,Output,Name):
    return f"{Picard} AddOrReplaceReadGroups I={InBam}.sort.dedup.bam O={Output}/{Name}.sort.dedup.bam SO=coordinate ID={Name} LB={Name} PL=illumina PU={Name} SM={Name} CREATE_INDEX=true VALIDATION_STRINGENCY=LENIENT\n"
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-o','--output',type=str,help='The output file path',default='.')
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=6)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=10)
def main(input,output,queue,corenum,memory):
    '''
    CNOM-AGL08	IROO-VIG06
    '''
    if output[-1] == '/': output = output[:-1]
    for line in input:
        line = line.strip().split()
        Command = AddOrReplaceReadGroups(line[0],output,line[1])
#        print(Command)
        os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                         -q {queue} \
                         -n {corenum} \
                         -M {memory*1000000} \
                         -o {output}/{line[0]}.o \
                         -e {output}/{line[0]}.e \
                         -J {line[0]}.reheader \
                         {Command}')
if __name__ == '__main__':
    main()
