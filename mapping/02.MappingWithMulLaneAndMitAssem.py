# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Mon Jul  9 09:39:08 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''
# The format of input file must like: XXX.R1.fq.gz or XXX.R1.clean.fq.gz. If not, you can run 01.ChangeFastqFileNameInDir.py

import sys,os,logging,click,re

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

Picard = 'java -Xmx120g -Djava.io.tmpdir=/stor9000/apps/users/NWSUAF/2015050469/tmp -jar /stor9000/apps/users/NWSUAF/2015050469/software/picard-2.18.7.jar'
def BWAMEM(Name,Ref,Path,LeftFile,RightFile,Output):
    return f"#bwa mem -t 8 -M -R '@RG\\tID:{Name}\\tLB:{Name}\\tPL:ILLUMINA\\tSM:{Name}' {Ref} {Path}/{LeftFile} {Path}/{RightFile}|samtools view -q 10 -bS -F 0x4 - >{Output}/{Name}.bam\n"
def BWAMEMAndSortSam(Core,Name,Ref,Path,LeftFile,RightFile,Output):
    return f"bwa mem -t {Core} -M -R '@RG\\tID:{Name}\\tLB:{Name}\\tPL:ILLUMINA\\tSM:{Name}' {Ref} {Path}/{LeftFile} {Path}/{RightFile}|samtools view -b -F 0x4 - |{Picard} SortSam INPUT=/dev/stdin OUTPUT={Output}/{Name}.sort.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT\n"
def MergeSamFiles(Path,BamList,Name):
    Command = f"{Picard} MergeSamFiles"
    for bam in BamList: Command += f" I={Path}/{bam}.sort.bam"
    Command += f" SORT_ORDER=coordinate O={Path}/{Name}\_tmp.bam AS=true\n"
    return Command
def AddOrReplaceReadGroups(Path,Name):
    return f"{Picard} AddOrReplaceReadGroups I={Path}/{Name}\_tmp.bam O={Path}/{Name}.sort.bam SO=coordinate ID={Name} LB={Name} PL=illumina PU={Name} SM={Name} CREATE_INDEX=true VALIDATION_STRINGENCY=LENIENT\n"
def RemoveList(Path,BamList,Name):
    Command = ''
    if len(BamList) > 1:
        for Bam in BamList: Command += f'rm {Path}/{Bam}.sam\nrm {Path}/{Bam}.sort.bam\n'
        Command += f'rm {Path}/{Name}_dedup\nrm {Path}/{Name}_tmp.bam\nrm {Path}/{Name}.sort.bai\nrm {Path}/{Name}.sort.bam\n'
    else: Command += f'rm {Path}/{Name}_dedup\nrm {Path}/{Name}.sam\nrm {Path}/{Name}.sort.bam\n'
    return Command
def TransBamToFastq(Path,Name):
    return f"{Picard} SamToFastq INPUT={Path}/{Name}.sort.bam FASTQ={Path}/{Name}.fq INCLUDE_NON_PRIMARY_ALIGNMENTS=false INTERLEAVE=true VALIDATION_STRINGENCY=LENIENT\n"
#    return f"samtools view -F 0x4 {Path}/{Name}.bam |{Picard} SamToFastq INPUT=/dev/stdin FASTQ={Path}/{Name}.fq INCLUDE_NON_PRIMARY_ALIGNMENTS=false INTERLEAVE=true VALIDATION_STRINGENCY=LENIENT\n"
def MitAssemble(Ref,Path,Name):
    return f"mia -H 1 -F -i -c -r {Ref} -f {Path}/{Name}.fq -m {Path}/{Name}\n"
@click.command()
@click.option('-p','--path',type=str,help='The input file path',required=True)
@click.option('-r','--ref',type=str,help='The reference file',required=True)
@click.option('-i','--RefIndex',type=str,help='The index of reference file',required=True)
@click.option('-o','--output',type=str,help='The output file path',required=True)
@click.option('-q','--queue',type=click.Choice(['cpu6130','jynodequeue','jyqueue','mem128queue','denovoqueue']),help='The job queue',default='mem128queue')
@click.option('-c','--corenum',type=int,help='The core number of job',default=12)
@click.option('-m','--memory',type=int,help='The memory of job (Gb)',default=120)
def main(path,ref,refindex,output,queue,corenum,memory):
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
    if not os.path.exists(f'{output}/shell'): os.system(f'mkdir {output}/shell')
    OUTPUT = open(f'{output}/shell/{DirName}.mapping.sh','w')
    OUTPUT.write('#/bin/bash\n')
#    '''
    if len(LeftFile) == 1:
#        OUTPUT.write(BWAMEM(DirName,refindex,path,LeftFile[0],RightFile[0],output))
        OUTPUT.write(BWAMEMAndSortSam(corenum,DirName,refindex,path,LeftFile[0],RightFile[0],output))
        OUTPUT.write(f"echo {DirName} mapping finished!\n")
    else:
        for i in range(len(LeftFile)):
            FileName = LeftFile[i].split('.')[0]
#            OUTPUT.write(BWAMEM(FileName,refindex,path,LeftFile[i],RightFile[i],output))
            OUTPUT.write(BWAMEMAndSortSam(corenum,FileName,refindex,path,LeftFile[i],RightFile[i],output))
            OUTPUT.write(f"echo {FileName} mapping finished!\n")
            BamList.append(FileName)
        OUTPUT.write(MergeSamFiles(output,BamList,DirName))
        OUTPUT.write(AddOrReplaceReadGroups(output,DirName))
        OUTPUT.write(f"echo {DirName} merge finished!\n")
    #OUTPUT.write(RemoveList(output,BamList,DirName))
#    '''
    OUTPUT.write(TransBamToFastq(output,DirName))
    OUTPUT.write(MitAssemble(ref,output,DirName))
    os.system(f'chmod 755 {output}/shell/{DirName}.mapping.sh')

###### submit
    os.system(f'jsub -R "rusage[res=1]span[hosts=1]" \
                     -q {queue} \
                     -n {corenum} \
                     -M {memory*1000000} \
                     -o {output}/shell/{DirName}.o \
                     -e {output}/shell/{DirName}.e \
                     -J {DirName}.mit.ass \
                     {output}/shell/{DirName}.mapping.sh')
if __name__ == '__main__':
    main()
