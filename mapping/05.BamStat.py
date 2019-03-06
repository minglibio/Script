# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Wed Jul 18 14:50:11 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def HandleOutput(path):
    FileList = sorted(os.listdir(path))
    for file in FileList:
        FileName = file.split('.')[0]
        if not os.path.exists(f'{path}/{FileName}'): os.system(f'rm {path}/{file}')
@click.command()
@click.option('-p','--path',type=str,help='The path of bam file',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=4)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=40)
def main(path,queue,corenum,memory):
    if path[-1] == '/' : path = path[:-1]
    if not os.path.exists(f'{path}/BamStat'): os.system(f'mkdir -p {path}/BamStat')
    output = f'{path}/BamStat'
    HandleOutput(output)
    BamStatList = open(f'{output}/BamStat.list','w')
    FileList = sorted(os.listdir(path))
    for file in FileList:
        if file[-3:] != 'bam': continue
        FileName = file.split('.')[0]
        BamStatList.write(f'./{FileName}\n')
        if os.path.exists(f'{output}/{FileName}') : continue
        print(FileName)
        Command = f'qualimap bamqc -bam {path}/{file} -outdir {output}/{FileName} -outformat HTML --java-mem-size={int(memory)}G'
        os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                         -q {queue} \
                         -n {corenum} \
                         -M {memory*1000000} \
                         -o {output}/{FileName}.o \
                         -e {output}/{FileName}.e \
                         -J {FileName}.BamStat \
                         {Command}')
if __name__ == '__main__':
    main()
