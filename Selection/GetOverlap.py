# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Wed Nov 14 21:24:45 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
def LoadFiles(files):
  '''
  11      1415000 1480000 65000
  11      4055000 4065000 10000
  11      4480000 4495000 15000
  '''
  Dict = {}
  for line in files:
    line = line.strip().split()
    #print(line[0])
    Dict.setdefault(line[0],[]).append(line[1:])
  return Dict

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-i1','--input1',type=click.File('r'),help='The input file',required=True)
@click.option('-i2','--input2',type=click.File('r'),help='The input file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(input1,input2,output):
  LoadFile1 = LoadFiles(input1)
  for line in input2:
    line = line.strip().split()
    Overlap = False
    for Pos in LoadFile1[line[0]]:
      if line[1] <= Pos[1] <= line[2] or line[1] <= Pos[2] <= line[2]:
        Overlap = True
    if Overlap: output.write(f'{line[0]}\t{line[1]}\t{line[2]}\t{line[3]}\n')
    
if __name__ == '__main__':
    main()
