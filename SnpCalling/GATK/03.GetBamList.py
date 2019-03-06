# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Sat Aug  4 20:18:09 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import math

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-p','--path',type=str,help='The path',required=True)
def main(path):
    if path[-1] == '/' : path = path[:-1]
    List = os.popen(f'ls -hlF {path}').readlines()
    for line in List:
        line = line.strip()
        if not line[-1] == '/' : continue
        region = line.split()[-1]
#        print(region)
        os.system(f"ls `pwd`/{region}*.bam > {region}Bam.list")
        os.system(f"wc -l {region}Bam.list")
if __name__ == '__main__':
    main()
