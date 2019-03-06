#!/bin/bash
while getopts "n:N:" arg
do
    case $arg in
        n)
          FILE=$OPTARG
          ;;
        N)
          FILE=$OPTARG
          ;;
        ?)
          echo "unknow argument"
          exit 1
          ;;
    esac
done
########################
cat <<EOF> $PWD/${FILE}.py
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on `date`
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,output):
    
if __name__ == '__main__':
    main()
EOF
