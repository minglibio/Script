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

def ReturnInput(List):
    Input = ['' for _ in range(len(List))]
    StartPosList = []
    Dict = {}
    for VCF in List:
        StartPos = VCF.split(':')[1].split('-')[0]
        StartPosList.append(int(StartPos))
        Dict[VCF] = int(StartPos)
        StartPosList.sort()
    for VCF in Dict.keys():
        Input[StartPosList.index(Dict[VCF])] = VCF
    return ' '.join(Input)
@click.command()
@click.option('-i','--input',type=str,help='The path of VCF file (.gz file)',required=True)
@click.option('-o','--output',type=str,help='The path of output file',required=True)
@click.option('-p','--prefix',type=str,help='The prefix of output file',default='BCFtools')
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=4)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=25)
def main(input,output,prefix,queue,corenum,memory):
    if input[-1] == '/' : input = input[:-1]
    if output[-1] == '/' : output = output[:-1]
    VCFList = os.popen(f'ls  {input}/*.vcf.gz').readlines()
    VCFDict = {}
    for VCF in VCFList:
        VCF = VCF.strip()
        Chr = VCF.split(':')[0].split('.')[-1]
        VCFDict.setdefault(Chr,[]).append(VCF)
    for Chr,VCFList in VCFDict.items():
        VCFList = ReturnInput(VCFList)
        os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                    -q {queue} \
                    -n {corenum} \
                    -M {memory*1000000} \
                    -o {output}/{prefix}.{Chr}.o \
                    -e {output}/{prefix}.{Chr}.e \
                    -J ConcatVCF.{prefix}.{Chr} \
                    bcftools concat {VCFList} --threads {corenum} -O z -o {prefix}.{Chr}.vcf.gz')
if __name__ == '__main__':
    main()
