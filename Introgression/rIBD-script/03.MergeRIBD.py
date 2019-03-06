# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Wed Aug 15 17:18:03 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadControl(file):
    Dict = {}
    for line in file:
        if line.startswith('CHR'):continue
        line = line.strip().split()
        Index =f'{line[0]}{line[1]}'
        Dict[Index] = float(line[-1])
    return Dict
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-c','--control',type=click.File('r'),help='The control file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,control,output):
    Control = LoadControl(control)
    for line in input:
        if line.startswith('CHR'):continue
        line = line.strip().split()
        Index =f'{line[0]}{line[1]}'
        rIBD = float(line[-1]) - Control.setdefault(Index,0)
        output.write(f'{line[0]}\t{line[1]}\t{line[2]}\t{rIBD}\n')
if __name__ == '__main__':
    main()
