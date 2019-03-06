# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Mon Aug 13 20:21:18 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadIndividual(file):
    Dict = {}
    for line in file:
        line = line.strip()
        Dict[line] = None
    return Dict
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('--keep',type=click.File('r'),help='The input file')
@click.option('--remove',type=click.File('r'),help='The input file')
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,keep,remove,output):
    if keep:
        Sample = LoadIndividual(keep)
        for line in input:
            if line.split()[0] not in Sample: continue
            output.write(line)
    if remove:
        Sample = LoadIndividual(remove)
        for line in input:
            if line.split()[0] in Sample: continue
            output.write(line)
if __name__ == '__main__':
    main()
