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
@click.option('-l','--list',type=click.File('r'),help='The file of bam list',required=True)
@click.option('-y','--ylim',type=int,help='The file of bam list',default=30)
@click.option('-o','--output',type=str,help='The output file',required=True)
def main(list,ylim,output):
    if output[-1] == '/' : output = output[:-1]
    for line in list:
        line = line.strip()
        Name = line.split('/')[-1].split('.')[0]
        os.system(f'psmc_plot.pl -Y {ylim} -g 2 -u 4.32e-09 -p {Name} {output}/{Name}/combined.psmc')
if __name__ == '__main__':
    main()
