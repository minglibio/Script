# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Tue Mar  5 16:19:58 CST 2019
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click
import random,re

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadFa(File):
    FaDict,LenDict,NDict,seq = {}, {}, {}, ''
    for line in File:
        line = line.strip()
        if line[0] == '>':
            if len(seq) > 0:
                FaDict[name] = seq
                LenDict[name] = len(seq)
                NDict[name] = [[m.start(0), m.end(0)] for m in re.finditer('N+', seq)]
            name = line.split()[0][1:]
            seq = ''
        else: seq += line
    FaDict[name] = seq
    LenDict[name] = len(seq)
    NDict[name] = [[m.start(0), m.end(0)] for m in re.finditer('N+', seq)]
    return FaDict,LenDict,NDict
def GeneratedDeletionSeq(size):
    DeletionSeq = ''
    while len(DeletionSeq) < size:
        DeletionSeq += random.choice(['A','T','C','G'])
    return DeletionSeq
def GeneratedRegion(ChrLenDict,size,VarNum):
    Chr = random.choice(list(ChrLenDict.keys()))
    while len(Chr) > 5 or ChrLenDict[Chr]-VarNum*size < VarNum*size : Chr = random.choice(list(ChrLenDict.keys()))
    start = random.randint(1,ChrLenDict[Chr]-VarNum*size)
    Region = [start,start + size - 1]
    return Chr,Region
def Overlap(QueryList,SubjectList,size):
    for SubList in SubjectList:
        SubList = [SubList[0]-size,SubList[1]+size]
        if SubList[0] <= QueryList[0] <= SubList[1] or SubList[0] <= QueryList[1] <= SubList[1]: return True
    return False
def ChangeCoordinate(NewRegion,RegionList,size,Insertion):
    NewRegionList = []
    for region in RegionList:
        if Insertion and region[0] > NewRegion[1] : NewRegionList.append([region[0]-size,region[1]-size])
        elif region[0] > NewRegion[1] : NewRegionList.append([region[0]+size,region[1]+size])
        else:  NewRegionList.append(region)
    return NewRegionList
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-o','--output',type=str,help='The prefix of output file',required=True)
@click.option('-s','--size',type=int,help='The size of variations',default=2000)
@click.option('--insertion',type=int,help='The number of insertion',default=100)
@click.option('--deletion',type=int,help='The number of deletion',default=100)
@click.option('--inversion',type=int,help='The number of inversion',default=100)
@click.option('--translocation',type=int,help='The number of balanced translocation',default=100)
def main(input,output,size,insertion,deletion,inversion,translocation):
    Fa,Len,NDict = LoadFa(input)
    random.seed(100)
    VariationDict = {}
    #### add deletion variations on reference
    DeletionDict,DeletionNum = {},0
    DeletionSeq = GeneratedDeletionSeq(size)
    logging.info(f"The deletion sequence length is: {len(DeletionSeq)}\nThe deletion sequence is: {DeletionSeq}")
    while DeletionNum < deletion:
        Chr,Deletion = GeneratedRegion(Len,size,0)
        if Overlap(Deletion,NDict[Chr],size): continue
        if Chr in VariationDict and Overlap(Deletion,VariationDict[Chr],size): continue
        Fa[Chr] = Fa[Chr][:Deletion[0]-1] + DeletionSeq + Fa[Chr][Deletion[0]-1:]
        VariationDict.setdefault(Chr,[]).append(Deletion)
        DeletionDict.setdefault(Chr,[]).append(Deletion)
        if Chr in VariationDict:
            VariationDict[Chr] = ChangeCoordinate(Deletion,VariationDict[Chr],size,False)
            DeletionDict[Chr] = ChangeCoordinate(Deletion,DeletionDict[Chr],size,False)
            NDict[Chr] = ChangeCoordinate(Deletion,NDict[Chr],size,False)
        DeletionNum += 1
    #### add insertion variations on reference
    InsertionDict,InsertionNum = {},0
    while InsertionNum < insertion:
        Chr,Insertion = GeneratedRegion(Len,size,insertion)
        Insertion = [Insertion[0],Insertion[0]+1]
        if Overlap(Insertion,NDict[Chr],size): continue
        if Chr in VariationDict and Overlap(Insertion,VariationDict[Chr],size): continue
        Fa[Chr] = Fa[Chr][:Insertion[0]-1] + Fa[Chr][Insertion[0]-1+size:]
        VariationDict.setdefault(Chr,[]).append(Insertion)
        InsertionDict.setdefault(Chr,[]).append(Insertion)
        if Chr in VariationDict:
            VariationDict[Chr] = ChangeCoordinate(Insertion,VariationDict[Chr],size,True)
            InsertionDict[Chr] = ChangeCoordinate(Insertion,InsertionDict[Chr],size,True)
            NDict[Chr] = ChangeCoordinate(Insertion,NDict[Chr],size,True)
        InsertionNum += 1
    #### add inversion variations on reference
    InversionDict,InversionNum = {},0
    while InversionNum < inversion:
        Chr,Inversion = GeneratedRegion(Len,size,insertion)
        if Overlap(Inversion,NDict[Chr],size): continue
        if Chr in VariationDict and Overlap(Inversion,VariationDict[Chr],size): continue
        Fa[Chr] = Fa[Chr][:Inversion[0]-1] + Fa[Chr][Inversion[0]-1:Inversion[1]][::-1] + Fa[Chr][Inversion[1]:]
        VariationDict.setdefault(Chr,[]).append(Inversion)
        InversionDict.setdefault(Chr,[]).append(Inversion)
        InversionNum += 1
    #### add balanced translocation variations on reference
    TranslocationDict,TranslocationNum = {},0
    while TranslocationNum < translocation:
        Chr1,Translocation1 = GeneratedRegion(Len,size,insertion)
        Chr2,Translocation2 = GeneratedRegion(Len,size,insertion)
        if Overlap(Translocation1,NDict[Chr],size) or Overlap(Translocation2,NDict[Chr],size): continue
        if Chr1 in VariationDict and Overlap(Translocation1,VariationDict[Chr],size): continue
        if Chr2 in VariationDict and Overlap(Translocation2,VariationDict[Chr],size): continue
        Fa[Chr1] = Fa[Chr1][:Translocation1[0]-1] + Fa[Chr2][Translocation2[0]-1:Translocation2[1]] + Fa[Chr1][Translocation1[1]:]
        Fa[Chr2] = Fa[Chr2][:Translocation2[0]-1] + Fa[Chr1][Translocation1[0]-1:Translocation1[1]] + Fa[Chr2][Translocation2[1]:]
        VariationDict.setdefault(Chr1,[]).append(Translocation1)
        TranslocationDict.setdefault(Chr1,[]).append(Translocation1)
        VariationDict.setdefault(Chr2,[]).append(Translocation2)
        TranslocationDict.setdefault(Chr2,[]).append(Translocation2)
        TranslocationNum += 1

    #### output
    VarList = open(f'{output}.var','w')
    for key,value in DeletionDict.items():
        for region in value:
           VarList.write(f'{key}\t{region[0]}\t{region[1]}\tDEL\n')
    for key,value in InsertionDict.items():
        for region in value:
           VarList.write(f'{key}\t{region[0]}\t{region[1]}\tINS\n')
    for key,value in InversionDict.items():
        for region in value:
           VarList.write(f'{key}\t{region[0]}\t{region[1]}\tINV\n')
    for key,value in TranslocationDict.items():
        for region in value:
           VarList.write(f'{key}\t{region[0]}\t{region[1]}\tTRA\n')
    
    FaOut = open(f'{output}.fa','w')
    for key,value in Fa.items():
        FaOut.write(f'>{key}\n{value}\n')
    
    VarList.close()
    FaOut.close()
    
    logging.info(f"Since a complete truth set of SVs is not available for this genome, we modified the reference \
genome to introduce {insertion + deletion + inversion + 2*translocation} homozygous SVs at random locations: \
{insertion} insertion(s) (by deleting from the reference), {deletion} deletion(s) (by adding new sequence), {inversion} \
inversion(s), and {translocation} balanced translocation(s) creating {2*translocation} translocation events. The mean \
indel and inversion size was {size/1000}kb. We did not attempt to simulate tandem duplications, as this would \
require detecting and modifying tandem duplications preexisting in the reference.")
if __name__ == '__main__':
    main()
