# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Tue Aug  7 09:23:40 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import re

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-p','--path',type=str,help="The path of job's output file",required=True)
#@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(path):
    if path[-1] == '/' : path = path[:-1]
    OutputFileList = os.popen(f"ls {path}/*.o")
    CompletedJobs,ErrorJobs = 0,0
    for OutputFile in OutputFileList:
        OutputFile = OutputFile.strip()
        File = open(OutputFile)
        for line in File:
            line = line.strip()
            if line.startswith('Subject:'):
                Stat = line.split()[-1]
                if Stat == 'Done': CompletedJobs += 1
                else: ErrorJobs += 1
                Jobs = re.search('(?<=<).*(?=>)',line).group()
        print(f'{Jobs}:\t{Stat}')
    print(f'Completed:\t{CompletedJobs}\nError:\t{ErrorJobs}')
    
if __name__ == '__main__':
    main()
