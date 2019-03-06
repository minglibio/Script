# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Tue Jul  3 09:18:59 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,output):
    Dict = {}
    Total = 0
    for line in input:
        line = line.strip().split()
        Dict.setdefault(line[0],0)
        Dict[line[0]] += 1
        Total += 1

    output.write(f'Supplementary Table X. Distribution of SNPs within various genomic regions\n')
    output.write(f'Category\tSNP Count\n')
    for key,value in Dict.items():
        output.write(f'{key}\t{value}\n')
    output.write(f'Total: {Total}\n')
if __name__ == '__main__':
    main()
