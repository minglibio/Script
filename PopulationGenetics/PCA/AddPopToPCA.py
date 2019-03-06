# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Mon Aug 13 11:28:13 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadSample(File):
    Dict = {}
    for line in File:
        line = line.strip().split()
        Dict[line[0]] = line[2]
    return Dict
@click.command()
@click.option('-s','--sample',type=click.File('r'),help='The sample info file',required=True)
@click.option('-p','--pca',type=click.File('r'),help='The PCA file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(sample,pca,output):
    Sample = LoadSample(sample)
    for line in pca:
        line = line.strip().split()
        output.write(f'{line[0]}\t{line[2]}\t{line[3]}\t{line[4]}\t{Sample[line[0]]}\n')
if __name__ == '__main__':
    main()
