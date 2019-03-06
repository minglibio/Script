# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Sat Aug  4 21:42:14 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import math

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-p','--path',type=str,help='The BAM file Parent path',default='.')
def main(path):
    FileList = os.popen(f'find {path} -name *.e').readlines()
    for file in FileList :
        file = file.strip()
if __name__ == '__main__' :
    main()
