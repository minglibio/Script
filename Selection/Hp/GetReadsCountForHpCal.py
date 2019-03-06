# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Thu Mar  1 20:27:57 2018
@Mail: minnglee@163.com
@Author: Ming Li
"""

import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadSample(File):
    Dict = {}
    for line in File:
        line = line.strip()
        Dict[line] = None
    return Dict
@click.command()
@click.option('-i','--input',help='Input file',type=str,required=True)
@click.option('-S','--sample',help='Sample List file',type=click.File('r'),required=True)
@click.option('-o','--output',help='Output file',type=click.File('w'),required=True)
def main(input,sample,output):
    output.write('CHR\tPos\tRef\tAlt\n')
    INPUT = os.popen(f'less {input}')
    SampleDict = LoadSample(sample)
    SampleIndex = []
    for line in INPUT:
        line = line.strip()
        if line.startswith('##'): continue
        if line.startswith('Chr'):
            line = line.strip().split()
            for i in range(4,len(line)):
                if line[i] in SampleDict:
                    SampleIndex.append(line.index(line[i]))
            continue
        else:
            line = line.strip().split()
            SumRef = 0
            SumAlt = 0
            output.write(f'{line[0]}\t{line[1]}')
            for i in SampleIndex:
                ReadsCount = line[i].split('/')
                SumRef += int(ReadsCount[0])
                SumAlt += int(ReadsCount[1])
            output.write(f'\t{SumRef}\t{SumAlt}\n')
if __name__ == '__main__':
    main()
