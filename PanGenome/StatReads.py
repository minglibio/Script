# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Tue Oct 16 23:08:28 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import gzip
logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-i','--input',type=str,help='The input file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,output):
    File = gzip.open(input,'rb')
    TotalReads,TotalBase,GC = 0,0,0
    for line in File:
        line = line.decode().strip()
        if line.startswith('>'): continue
        TotalReads += 1
        TotalBase += len(line)
        GC += line.count('G')
        GC += line.count('C')
    output.write(f'Total Reads:\t{TotalReads}\n')
    output.write(f'Total base:\t{TotalBase}\n')
    output.write(f'GC base:\t{GC}\n')
    output.write(f'GC Ratio:\t{round(GC/TotalBase,4)}\n')
if __name__ == '__main__':
    main()
