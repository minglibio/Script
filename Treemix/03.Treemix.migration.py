# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Sun Aug 19 22:25:06 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-i','--input',type=str,help='input file',required=True)
@click.option('-k','--number',type=int,help='number of SNPs per block for estimation of covariance matrix',default=500)
@click.option('--migration',type=int,help='number of migration edges to add',default=20)
@click.option('--root',type=str,help='comma-delimited list of populations to set on one side of the root (for migration)',default='Outgroup')
@click.option('-o','--output',type=str,help='The path of output file',default='./migration')
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='mem128queue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=2)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=20)
def main(input,number,migration,root,output,queue,corenum,memory):
    if output[-1] == '/' : output = output[:-1]
    if not os.path.exists(output): os.system(f'mkdir {output}')
    for i in range(1,migration+1):
        print(i)
#'''
        os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                     -q {queue} \
                     -n {corenum} \
                     -M {memory*1000000} \
                     -o {output}/migration_{i}.o \
                     -e {output}/migration_{i}.e \
                     -J treemix.migration_{i} \
                     treemix -i {input} -m {i} -k {number} -root {root} -o {output}/migration_{i}')
#'''
if __name__ == '__main__':
    main()
