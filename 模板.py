#!/usr/bin/env python3

'''
------------------------------------------------------------------------------------------
Author: Ming Li
Email: minnglee@163.com
Time: 2016/1/7
Version: 1.0
------------------------------------------------------------------------------------------
'''

import sys
import getopt
import os
import time
import re

def usage():
    print(__doc__)
    print('''Usage: python script.py [option] [parameter]
    -i/--InputFile             the input file
    -o/--OutputFile            the output file
    -h/--help                  show possible options
------------------------------------------------------------------------------------------''')
def GetCommandLine():
    CommandLine=' '.join(sys.argv)
    CommandLine='python3 '+CommandLine
    return(CommandLine)
def log(LogInfo):
    CurrentFolder=os.popen('pwd').read().strip()
    LogFileName=re.split('/|\\\\',sys.argv[0].strip())
    LogFileName=LogFileName[-1].split('.')
    LogFileName=LogFileName[0]+'.log'
    LogFile=open(CurrentFolder+'/'+LogFileName,'a')
    LogFile.write(LogInfo+'\n')
    LogFile.close()
def LoadFasta(file):
    dict={}
    seq=''
    for line in file:
        line=line.strip()
        if line[0] == '>':
            if len(seq) > 0:
                dict[name]=seq
            temp=line.split()
            name=temp[0][1:]
            seq=''
        else:
            seq+=line
    dict[name]=seq
    file.close()
    return dict
def main():
    log('The start time: '+time.ctime())
    log('The command line is:\n'+GetCommandLine())
    xxx()
    log('The end time: '+time.ctime())    
#############################default

#############################
opts,argvs=getopt.getopt(sys.argv[1:],'hi:o:',['help','InputFile=','OutputFile='])
for op,value in opts:
    if op=='-i' or op=='--InputFile':
        InputFile=open(value)
    elif op=='-o' or op=='--OutputFile':
        OutputFile=open(value,'w')
    elif op=='-h' or op=='--help':
        usage()
        sys.exit(1)
if len(sys.argv) == 1:
    usage()
    sys.exit(1)
###########################
if __name__=='__main__':
    main()