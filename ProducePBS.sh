#!/bin/bash
FILE=$1
########################
cat <<EOF> $PWD/${FILE}.py
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on `date`
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-o','--output',type=str,help='The output file',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=2)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=10)
def main(input,output,queue,corenum,memory):
    if not os.path.exists(f'{output}/shell'): os.system(f'mkdir {output}/shell')
    ShellName = f''
    OUTPUT = open(f'{output}/shell/{ShellName}.sh','w')
    OUTPUT.write('#/bin/bash\n')
    ###### submit
    os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \\
                     -q {queue} \\
                     -n {corenum} \\
                     -M {memory*1000000} \\
                     -o {output}/shell/{ShellName}.o \\
                     -e {output}/shell/{ShellName}.e \\
                     -J {ShellName} \\
                     {output}/shell/{ShellName}.sh')
if __name__ == '__main__':
    main()
EOF
