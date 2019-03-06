# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Mon Jul  9 09:39:08 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''
# The format of input file must like: XXX.R1.fq.gz or XXX.R1.clean.fq.gz. If not, you can run 01.ChangeFastqFileNameInDir.py

import sys,os,logging,click,re

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def BWAMEMAndSortSam(Picard,Core,Name,Ref,Path,LeftFile,RightFile,Output):
    return f"bwa mem -t {Core} -M -R '@RG\\tID:{Name}\\tLB:{Name}\\tPL:ILLUMINA\\tSM:{Name}' {Ref} {Path}/{LeftFile} {Path}/{RightFile} |{Picard} SortSam INPUT=/dev/stdin OUTPUT={Output}/{Name}.sort.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT\n"
def MergeSamFiles(Picard,Path,BamList,Name):
    Command = f"{Picard} MergeSamFiles"
    for bam in BamList: Command += f" I={Path}/{bam}.sort.bam"
    Command += f" SORT_ORDER=coordinate O={Path}/{Name}_tmp.bam AS=true\n"
    return Command
def AddOrReplaceReadGroups(Picard,Path,Name):
    return f"{Picard} AddOrReplaceReadGroups I={Path}/{Name}_tmp.bam O={Path}/{Name}.sort.bam SO=coordinate ID={Name} LB={Name} PL=illumina PU={Name} SM={Name} CREATE_INDEX=true VALIDATION_STRINGENCY=LENIENT\n"
@click.command()
@click.option('-p','--path',type=str,help='The input file path',required=True)
@click.option('-r','--ref',type=str,help='The reference file',required=True)
@click.option('-o','--output',type=str,help='The output file path',default='.')
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='mem128queue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=12)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=120)
def main(path,ref,output,queue,corenum,memory):
    Picard = f'java -Xmx{memory}g -Djava.io.tmpdir=/stor9000/apps/users/NWSUAF/2015050469/tmp -jar /stor9000/apps/users/NWSUAF/2015050469/software/picard-2.18.7.jar'
    LeftFile,RightFile = [],[]
    BamList = []
    FileList = sorted(os.listdir(path))
    for File in FileList:
        if re.search('\.R1\.',File): LeftFile.append(File)
        elif re.search('\.R2\.',File):RightFile.append(File)
    if path[-1] == '/' : path = path[:-1]
    DirName = path.split('/')[-1]
    print(DirName)
    if output[-1] == '/': output = output[:-1]
    ScriptDir = f'{output}/shell'
    if not os.path.exists(f'{ScriptDir}'): os.system(f'mkdir -p {ScriptDir}')
    ShellName = f'{DirName}.mapping.sh'
    OUTPUT = open(f'{ScriptDir}/{ShellName}','w')
    OUTPUT.write(f"#!/bin/bash\n")
    if len(LeftFile) == 1:
        OUTPUT.write(BWAMEMAndSortSam(Picard,corenum,DirName,ref,path,LeftFile[0],RightFile[0],output))
        OUTPUT.write(f"echo {DirName} mapping and sort finished!\n")
    else:
        for i in range(len(LeftFile)):
            FileName = LeftFile[i].split('.')[0]
            OUTPUT.write(BWAMEMAndSortSam(Picard,corenum,FileName,ref,path,LeftFile[i],RightFile[i],output))
            OUTPUT.write(f"echo {FileName} mapping and sort finished!\n\n")
            BamList.append(FileName)
        OUTPUT.write(MergeSamFiles(Picard,output,BamList,DirName))
        OUTPUT.write(AddOrReplaceReadGroups(Picard,output,DirName))
        OUTPUT.write(f"echo {DirName} merge finished!\n")
    os.system(f'chmod 755 {ScriptDir}/{ShellName}')
#'''
    os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                     -q {queue} \
                     -n {corenum} \
                     -M {memory*1000000} \
                     -o {ScriptDir}/{DirName}.o \
                     -e {ScriptDir}/{DirName}.e \
                     -J {DirName}.mapping \
                     {ScriptDir}/{ShellName}')
#'''
if __name__ == '__main__':
    main()
