# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Wed Jan 16 17:50:59 CST 2019
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def Rename(name):
    return f'{name.split(":")[0]}#{name.split(":")[1].replace("-","#")}'
def LoadFasta(File):
    Dict = {}
    seq = ''
    for line in File:
        line = line.strip()
        if line[0] == '>':
            if len(seq) > 0:
                Dict[name] = seq
            name = Rename(line.split()[0][1:])
            seq = ''
        else: seq += line
    Dict[name] = seq
    return Dict
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-l','--length',type=int,help='the min length of seqence',default=500)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,length,output):
    FaDict = LoadFasta(input)
    for key,value in FaDict.items():
        Gap = value.upper().count('N')
        if len(value) - Gap < length : continue
        while value[0].upper() == "N": value = value[1:]
        while value[-1].upper() == "N": value = value[:-1]
        output.write(f'>{key}\n{value}\n')
if __name__ == '__main__':
    main()
