# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Wed Jul 18 15:09:49 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import re

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def HandleOutput(path):
    FileList = sorted(os.listdir(path))
    for file in FileList:
        FileName = file.split('.')[0]
        if not os.path.exists(f'{path}/{FileName}.o'): os.system(f'rm {path}/{file}')
@click.command()
@click.option('-p','--path',type=str,help='The path of bam check result files',required=True)
def main(path):
    if path[-1] == '/' : path = path[:-1]
    BadFile = open(f'{path}/File.Bad','w')
    FileStat = open(f'{path}/File.Stat','w')
    FileList = sorted(os.listdir(path))
    for file in FileList:
        FileName = file.split('.')[0]
        if file[-2:] == '.e':
            if os.path.getsize(f'{path}/{file}') > 0:
                BadFile.write(f'{FileName}\n')
        if file[-2:] == '.o':
            Mapped = os.popen(f'grep "mapped (" {path}/{file}').read()
            MappedRatio = re.search('(?<=mapped \().*(?=%)',Mapped).group()
            FileStat.write(f'{FileName}\t{MappedRatio}\n')
if __name__ == '__main__':
    main()
