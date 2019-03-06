# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Mon Dec 24 16:22:00 CST 2018
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
    '''
    E00510:287:HJLHWCCXY:8:1101:3244:2680   gi|970750704|ref|XM_015234391.1|        94.44   72      4       0       1       72      173     102     1e-21   111     Vicugna pacos|Vicugna|Camelidae|NA|Mammalia|Chordata|Eukaryota|
    E00510:287:HJLHWCCXY:8:1101:5091:2680   gi|970698884|ref|XM_015243814.1|        97.93   145     3       0       1       145     409     553     2e-63   252     Vicugna pacos|Vicugna|Camelidae|NA|Mammalia|Chordata|Eukaryota|
    E00510:287:HJLHWCCXY:8:1101:6187:2680   gi|223972289|dbj|AP003423.1|    99.30   142     1       0       1       142     9100    8959    3e-65   257     Camelus bactrianus|Camelus|Camelidae|NA|Mammalia|Chordata|Eukaryota|
    '''
    Dict = {}
    for line in input:
        line = line.strip().split('\t')
        Name = line[-1].split('|')[0]
        if Name not in Dict: Dict[Name] = 0
        Dict[Name] +=1
    DictList = sorted(Dict.items(),key=lambda t:t[1],reverse=True)
    for species in DictList:
        output.write(f'{species[0]}\t{species[1]}\n')    
if __name__ == '__main__':
    main()
