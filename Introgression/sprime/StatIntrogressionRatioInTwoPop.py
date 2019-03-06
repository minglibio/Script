# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Tue Apr 24 11:12:01 2018
@Mail: minnglee@163.com
@Author: Ming Li
"""

import sys,os,argparse,time,re
import matplotlib.pyplot as plt

def GetCommandLine():
    CommandLine='python3 {0}'.format(' '.join(sys.argv))
    return(CommandLine)
LogFile=None
def log(LogInfo):
    '''
    Output the LogInfo to log file
    '''
    global LogFile
    if sys.platform == 'linux':
        CurrentFolder=os.getcwd()
        LogFileName=re.split('/|\\\\',sys.argv[0].strip())
        LogFileName=LogFileName[-1].split('.')
        LogFileName='{0}/{1}.log'.format(CurrentFolder,LogFileName[0])
        if LogFile:LogFile.write(LogInfo+'\n')
        else:
            LogFile=open(LogFileName,'w')
            LogFile.write(LogInfo+'\n')
    else:
        print(LogInfo)
def LoadSample(File):
    Dict = {}
    FILE = open(File)
    for line in FILE:
        line = line.strip()
        Dict[line] = None
    return Dict
def HandleHeader(line):
    Pop1Dict = LoadSample(args.Pop1)
    Pop2Dict = LoadSample(args.Pop2)
    Pop1Index,Pop2Index = [],[]
    line = line.strip().split()
    for i in range(len(line)):
        if line[i] in Pop1Dict:
            Pop1Index.append(line.index(line[i]))
        elif line[i] in Pop2Dict:
            Pop2Index.append(line.index(line[i]))
    return Pop1Index,Pop2Index
def plot(x,y):
    plt.switch_backend('pdf') #matplotlib的默认backend是TkAgg，而FltkAgg, GTK, GTKAgg, GTKCairo, TkAgg , Wx or WxAgg这几个backend都要求有GUI图形界面的，所以在ssh操作的时候会报错．解决方法：指定不需要GUI的backend（Agg, Cairo, PS, PDF or SVG）
#    plt.figure(figsize=(5,6))
#    x=[0.1,0.2,0.5,0.8]
#    y=[0.1,0.2,0.5,0.8]
#    Threshold_x = sorted(x,reverse=True)[int(len(x)/1000)]
#    Threshold_y = sorted(y,reverse=True)[int(len(y)/1000)]
    Threshold_x = 0.5
    Threshold_y = 0.5
    plt.title("Adaptive introgression") 
#    plt.xlim(xmax=7,xmin=0)
#    plt.ylim(ymin=0.2)
#    plt.ylim(ymax=7,ymin=0)
    plt.xlabel("Asian haplotype frequency")
    plt.ylabel("EUR-AFR haplotype frequency")
    plt.axvline(Threshold_x,0,1,color="black",linestyle="dashed",linewidth=1)
    plt.axhline(Threshold_y,0,1,color="black",linestyle="dashed",linewidth=1)
    plt.scatter(x,y,c="gray",s=10,alpha=1)
    plt.savefig('Sprime.total.Frq.Plot.pdf',format='pdf')
def StatIntrogressionRatioInTwoPop():
    '''
    #Chr    Segment     Start           End             TotalVar        A1              A14             A23             A25 
    1       0           4706531         37367666        14984           2639|2153       981|1521        1257|1576       1582|1749
    1       1           40591660        65818633        10529           1433|1486       704|693         1076|1055       1048|886
    '''
    args.output.write('#Chr\tSegment\tStart\tEnd\tTotalVar\tEA-SWA-SA_Frq\tAFR-EUR_Frq\n')
    PlotX = []
    PlotY = []
    for line in args.input:
        if line.startswith('#'):
            Pop1Index,Pop2Index = HandleHeader(line)
            continue
        Pop1Hap = 0
        Pop2Hap = 0
        line = line.strip().split()
        for i in range(5,len(line)):
            Hap = line[i].split('|')
            if int(Hap[0])/int(line[4]) > args.ratio and  int(Hap[0]) > args.number:
               if i in Pop1Index: Pop1Hap += 1
               elif i in Pop2Index: Pop2Hap += 1
            if int(Hap[1])/int(line[4]) > args.ratio and  int(Hap[1]) > args.number:
               if i in Pop1Index: Pop1Hap += 1
               elif i in Pop2Index: Pop2Hap += 1
        Pop1HapRatio = Pop1Hap/(len(Pop1Index)*2)
        Pop2HapRatio = Pop2Hap/(len(Pop2Index)*2)
        args.output.write('{0}\t{1}\t{2}\n'.format('\t'.join(line[:5]), Pop1HapRatio, Pop2HapRatio))
        PlotX.append(round(Pop1HapRatio,4))
        PlotY.append(round(Pop2HapRatio,4))
    plot(PlotX,PlotY)
def main():
    print('Running...')
    log('The start time: {0}'.format(time.ctime()))
    log('The command line is:\n{0}'.format(GetCommandLine()))
    StatIntrogressionRatioInTwoPop()
    log('The end time: {0}'.format(time.ctime()))
    print('Done!')
#############################Argument
parser=argparse.ArgumentParser(description=print(__doc__),formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i','--Input',metavar='File',dest='input',help='Input file',type=open,required=True)
parser.add_argument('-1','--Pop1',metavar='File',dest='Pop1',help='Pop 1 file',type=str,required=True)
parser.add_argument('-2','--Pop2',metavar='File',dest='Pop2',help='Pop 2 file',type=str,required=True)
parser.add_argument('-n','--number',metavar='INT',dest='number',help='The min number of introgressive variation',type=int,default=50)
parser.add_argument('-r','--ratio',metavar='FLOAT',dest='ratio',help='The min ratio of introgressive variation',type=float,default=0.2)
parser.add_argument('-o','--Output',metavar='File',dest='output',help='Output file',type=argparse.FileType('w'),required=True)
args=parser.parse_args()
###########################
if __name__=='__main__':
    main()