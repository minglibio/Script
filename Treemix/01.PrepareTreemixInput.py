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
@click.option('-s','--sample',type=str,help='The sample file',required=True)
@click.option('-b','--bed',type=str,help='The bed file of Plink',required=True)
@click.option('-n','--name',type=str,help='The name of output file',required=True)
@click.option('-o','--output',type=str,help='The path of output file',default='.')
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='jynodequeue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=8)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=80)
def main(sample,bed,name,output,queue,corenum,memory):
    Plink2Treemix = '~/script/Treemix/Plink2Treemix.py'
    
    if output[-1] == '/' : output = output[:-1]
    Shell = open(f'{output}/{name}.treemix.input.sh','w')

    Shell.write('#/bin/bash\n')
    Shell.write(f'plink --bfile {bed} --allow-extra-chr --chr-set 40 --freq --missing --within {sample} --out {name}\n')
    Shell.write(f'gzip -f {name}.frq.strat\n')
    Shell.write(f'python3 {Plink2Treemix} -i {name}.frq.strat.gz -o {name}.frq\n')
    os.system(f'chmod 755 {output}/{name}.treemix.input.sh')

###### submit
    os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                     -q {queue} \
                     -n {corenum} \
                     -M {memory*1000000} \
                     -o {output}/{name}.treemix.input.o \
                     -e {output}/{name}.treemix.input.e \
                     -J {name}.treemix.input \
                     {output}/{name}.treemix.input.sh')
if __name__ == '__main__':
    main()
