# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Sat Oct  6 21:47:22 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import numpy as np

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-i','--input',type=str,help='The input file',required=True)
@click.option('-m','--mu',type=float,help='The mutation ratio',default=4.32e-9)
@click.option('-g','--generation',type=float,help='The generation time',default=2)
@click.option('-c','--col',type=int,help='The column',default=1)
@click.option('-t','--theta',type=int,help='The column of theta',default=2)
@click.option('-r','--rho',type=int,help='The column of rho',default=3)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,mu,generation,col,theta,rho,output):
    if input[-1] == '/': input = input[:-1]
    Result = os.popen(f'AA=`ls {input}/*.result`;for i in $AA;do cat $i;done').readlines()
    TimeList = []
    for line in Result:
        line = line.strip().split()
        Time = (float(line[col-1])/mu)*generation
        if not 5000 < Time < 10000000 :continue
        Pop = float(line[theta-1])/mu/4
        if not 5000 < Pop < 1000000 : continue
        Rec = float(line[rho-1])/Pop/4*1000000
        if not 0.1 < Rec < 10 : continue
        output.write(f'{Time}\t{Pop}\t{Rec}\n')
        TimeList.append(Time)
    output.write(f'{np.mean(TimeList)}')
if __name__ == '__main__':
    main()
