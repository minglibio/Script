# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Thu Dec  6 20:11:59 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('--identity',type=float,help='The min identity',default=90)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,identity,output):
    '''bed 格式 [start end) 0 based'''
    for line in input:
        line = line.strip().split()
        if float(line[2]) <= identity: continue
        Chr = line[0].split(':')[0]
        Pos = line[0].split(':')[1].split('-')
        output.write(f'{Chr}\t{int(Pos[0])+int(line[7])-1}\t{int(Pos[0])+int(line[8])}\n') 
if __name__ == '__main__':
    main()
