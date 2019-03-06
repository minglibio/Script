# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Thu Apr 27 19:54:46 2017
@Mail: minnglee@163.com
@Author: Ming Li
"""

import sys,os,logging,click
import math

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadHp(File,SNPNum):
    '''
    CHROM	BIN_START	BIN_END	N_VARIANTS	PI
    chr1	1	40000	365	0.00244356
    chr1	10001	50000	450	0.00299203
    '''
    Dict = {}
    for line in File:
        if line.startswith('CHR'): continue
        line = line.strip().split()
        if int(line[3]) < SNPNum: continue
        line[0] = line[0].replace('chr', '')
        index = '{0}-{1}'.format(line[0],line[1])
        Dict[index] = float(line[4])
    return Dict
@click.command()
@click.option('-1','--input1',help='Input 1 file [wild]',type=click.File('r'),required=True)
@click.option('-2','--input2',help='Input 2 file [dom]',type=click.File('r'),required=True)
@click.option('--snp',help='The min SNP number',type=int,default=10)
@click.option('-o','--output',help='Output file',type=click.File('w'),required=True)
def main(input1,input2,snp,output):
    WildHp = LoadHp(input1,snp)
    for line in input2:
        if line.startswith('CHR'): continue
        line = line.strip().split()
        if line[0] == 'chrU':continue
        if line[0] == 'chrW':continue
        if line[0] == 'chrZ':continue
        if int(line[3]) < snp: continue
        line[0] = line[0].replace('chr', '')
        index = '{0}-{1}'.format(line[0],line[1])
        if index in WildHp:
            Pos = '\t'.join(line[:3])
            HpRatio = math.log(WildHp[index]/float(line[4]))
            output.write(f'{Pos}\t{HpRatio}\n')
if __name__ == '__main__':
    main()
