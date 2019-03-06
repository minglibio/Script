# -*- coding: utf-8 -*-
"""
Created on Fri May  4 21:43:23 2018
@Mail: minnglee@163.com
@Author: Ming Li
"""

import sys,os,logging
import click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info('The command line is:\n\t{0}'.format('python3 {0}'.format(' '.join(sys.argv))))

@click.command()
@click.option('-t','--trait',help='the name of trait',type=str)
@click.option('-i','--input',help='the input file',type=click.File('r'))
@click.option('-o','--output',help='the output file',type=click.File('w'))
def main(input,output,trait):
    output.write('CHR\tBP\tP\n')
    for line in input:
        line = line.strip().split()
        line[2].replace('X1','30')
        line[2].replace('X2','31')
        line[2].replace('X','27')
        if line[0] == trait and float(line[5]) > 0 :
            output.write(f'{line[2]}\t{line[3]}\t{line[5]}\n')
if __name__=='__main__':
    main()
