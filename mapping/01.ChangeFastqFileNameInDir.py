# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Thu Jul  5 09:41:25 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click,re

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def ReName(DirName,Fq):
    print(Fq)
    if not re.search('.gz',Fq) : return 0
    FqList = Fq.split('.')
    if FqList[0][-2:] == '_1' or FqList[0][-2:] == '_2':
        NewName = f"{FqList[0][:-2]}.R{FqList[0][-1]}.{'.'.join(FqList[1:])}"
    elif FqList[0][-2:] == '_R1' or FqList[0][-2:] == '_R2':
        NewName = f"{FqList[0][:-3]}.R{FqList[0][-1]}.{'.'.join(FqList[1:])}"
    NewName = NewName.replace('fastq','fq')
    print(NewName)
    os.system(f'mv {DirName}/{Fq} {DirName}/{NewName}')
def main():
    File = os.popen(f'ls -l *')
    for line in File:
#        if not re.search('.gz',line) : continue
        line = line.strip().split()
        if len(line) != 9:
            if len(line) == 0: continue
            elif line[0][-1] == ':': DirName = line[0][:-1]
        elif 'DirName' not in dir():
            ReName('.',line[8])
        else:
           ReName(DirName,line[8])
if __name__ == '__main__':
    main()
