# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Thu Apr 27 19:54:46 2017
@Mail: minnglee@163.com
@Author: Ming Li
"""
import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadValue(file,Column):
    '''
    CHROM	BIN_START	BIN_END	N_VARIANTS	WEIGHTED_FST
    1	1	40000	361	0.0615512
    1	10001	50000	443	0.0603516
    '''
    Dict = {}
    for line in file:
        if line.startswith('CHR'): continue
        if line.startswith('Chr'): continue
        line = line.strip().split()
        Dict.setdefault(line[0],[]).append([int(line[1]),float(line[(Column-1)])])
    return Dict
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-c','--column',type=int,help='The column',default=5)
@click.option('-r','--region',type=click.File('r'),help='The CDR file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input,column,region,output):
    '''
    1 	10950001 	11030000 
    1 	41820001 	41960000 
    '''
    ValueDict = LoadValue(input,column)
    for line in region:
        line = line.strip().split()
        List = ValueDict[line[0]]
        Value = []
        for win in List:
            if int(line[1]) - 2 <= win[0] <= int(line[2]) + 2:
                Value.append(win)
        ValueSort = sorted(Value,key=lambda x: -x[1])
        CDR = '\t'.join(line[:3])
        output.write(f"{CDR}\t{int(line[2])-int(line[1])}\t{ValueSort[0][0]}\t{ValueSort[0][1]}\n")
if __name__ == '__main__':
    main()
