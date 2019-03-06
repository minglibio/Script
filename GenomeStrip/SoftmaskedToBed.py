# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Sat Sep 15 19:31:52 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click,re

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadSeq(File):
    seq = ''
    for line in File:
        line = line.strip()
        if line[0] == '>':
            Chr = line.split()[0][1:]
            continue
        else: seq += line
    return Chr,seq
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
#@click.option('-o','--output',type=str,help='The prefix of output file',required=True)
def main(input):
    Chr,Seq = LoadSeq(input)
    Mask = [(m.start(0), m.end(0)) for m in re.finditer('1*', Seq)]
    Alignable = [(m.start(0), m.end(0)) for m in re.finditer('0*', Seq)]
    MaskFile = open(f'{Chr}.mask.region','w')
    for region in Mask:
        if int(region[1]) - int(region[0]) == 0: continue
        MaskFile.write(f'{Chr}\t{int(region[0])+1}\t{int(region[1])}\n')
    AlignableFile = open(f'{Chr}.alignable.region','w')
    for region in Alignable:
        if int(region[1]) - int(region[0]) == 0: continue
        AlignableFile.write(f'{Chr}\t{int(region[0])+1}\t{int(region[1])}\n')
if __name__ == '__main__':
    main()
