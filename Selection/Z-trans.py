# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Wed Sep 19 16:31:47 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import pandas as pd

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-c','--columns',type=int,help='The columns of data to Z-trans',default=4)
@click.option('-o','--output',type=str,help='The output file',required=True)
def main(input,columns,output):
    df = pd.read_table(input,sep="\t",low_memory=False)
    DataCol = df.columns[columns-1]
    col_zscore = f'{DataCol}_zscore'
    DataCol = df.columns[columns-1]
    print(DataCol)
    df[col_zscore] = (df[DataCol] - df[DataCol].mean())/df[DataCol].std(ddof=1) # sample standard deviation (ddof=1) or population standard deviation (ddof=0)
    df.to_csv(f'{output}.txt', index=False,header=True,sep="\t")
if __name__ == '__main__':
    main()
