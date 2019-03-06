# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Tue Apr 24 11:12:01 2018
@Mail: minnglee@163.com
@Author: Ming Li
"""
import sys,os,logging,click

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadSample(File):
    Dict = {}
    for line in File:
        line = line.strip()
        Dict[line] = None
    return Dict
def HandleHeader(line,Pop1Dict,Pop2Dict,Pop3Dict,Pop4Dict):
    Pop1Index,Pop2Index,Pop3Index,Pop4Index = [],[],[],[]
    line = line.strip().split()
    for i in range(len(line)):
        if line[i] in Pop1Dict:
            Pop1Index.append(line.index(line[i]))
        elif line[i] in Pop2Dict:
            Pop2Index.append(line.index(line[i]))
        elif line[i] in Pop3Dict:
            Pop3Index.append(line.index(line[i]))
        elif line[i] in Pop4Dict:
            Pop4Index.append(line.index(line[i]))
    return Pop1Index,Pop2Index,Pop3Index,Pop4Index
@click.command()
@click.option('-i','--input',type=click.File('r'),help='Tne Input file',required=True)
@click.option('-1','--pop1',type=click.File('r'),help='Pop 1 file',required=True)
@click.option('-2','--pop2',type=click.File('r'),help='Pop 2 file',required=True)
@click.option('-3','--pop3',type=click.File('r'),help='Pop 3 file',required=True)
@click.option('-4','--pop4',type=click.File('r'),help='Pop 4 file',required=True)
@click.option('-n','--number',type=int,help='The min number of introgressive variation',default=50)
@click.option('-r','--ratio',type=float,help='The min ratio of introgressive variation',default=0.2)
@click.option('-o','--output',help='Output file',type=click.File('w'),required=True)
def main(input,pop1,pop2,pop3,pop4,number,ratio,output):
    '''
    #Chr    Segment     Start           End             TotalVar        A1              A14             A23             A25 
    1       0           4706531         37367666        14984           2639|2153       981|1521        1257|1576       1582|1749
    1       1           40591660        65818633        10529           1433|1486       704|693         1076|1055       1048|886
    '''
    Pop1Dict = LoadSample(pop1)
    Pop2Dict = LoadSample(pop2)
    Pop3Dict = LoadSample(pop3)
    Pop4Dict = LoadSample(pop4)
    
    output.write('#Chr\tSegment\tStart\tEnd\tTotalVar\tEA_Frq\tSWA-SA_Frq\tEUR_Frq\tAFR_Frq\n')
    for line in input:
        if line.startswith('#'):
            Pop1Index,Pop2Index,Pop3Index,Pop4Index = HandleHeader(line,Pop1Dict,Pop2Dict,Pop3Dict,Pop4Dict)
            continue
        Pop1Hap,Pop2Hap,Pop3Hap,Pop4Hap = 0,0,0,0
        line = line.strip().split()
        for i in range(5,len(line)):
            Hap = line[i].split('|')
            if int(Hap[0])/int(line[4]) > ratio and  int(Hap[0]) > number:
               if i in Pop1Index: Pop1Hap += 1
               elif i in Pop2Index: Pop2Hap += 1
               elif i in Pop3Index: Pop3Hap += 1
               elif i in Pop4Index: Pop4Hap += 1
            if int(Hap[1])/int(line[4]) > ratio and  int(Hap[1]) > number:
               if i in Pop1Index: Pop1Hap += 1
               elif i in Pop2Index: Pop2Hap += 1
               elif i in Pop3Index: Pop3Hap += 1
               elif i in Pop4Index: Pop4Hap += 1
        Pop1HapRatio = Pop1Hap/(len(Pop1Index)*2)
        Pop2HapRatio = Pop2Hap/(len(Pop2Index)*2)
        Pop3HapRatio = Pop3Hap/(len(Pop3Index)*2)
        Pop4HapRatio = Pop4Hap/(len(Pop4Index)*2)
        Region = '\t'.join(line[:5])
        output.write(f'{Region}\t{Pop1HapRatio}\t{Pop2HapRatio}\t{Pop3HapRatio}\t{Pop4HapRatio}\n')
if __name__=='__main__':
    main()
