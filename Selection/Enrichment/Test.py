# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Wed Aug 22 16:03:13 CST 2018
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
    
if __name__ == '__main__':
    main()
