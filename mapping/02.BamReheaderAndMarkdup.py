# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Mon Jul  9 09:39:08 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''
# The format of input file must like: XXX.R1.fq.gz or XXX.R1.clean.fq.gz. If not, you can run 01.ChangeFastqFileNameInDir.py

import sys,os,logging,click,re

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

Picard = 'java -Xmx200g -Djava.io.tmpdir=/stor9000/apps/users/NWSUAF/2015050469/tmp -jar /stor9000/apps/users/NWSUAF/2012010954/Software/picard-tools-2.5.0/picard.jar'
Samtools='/stor9000/apps/users/NWSUAF/2012010954/Software/samtools1.7/bin/samtools'
def BWAMEMAndSortSam(Name,Ref,Path,LeftFile,RightFile,Output):
    return f"bwa mem -t 8 -M -R '@RG\\tID:{Name}\\tLB:{Name}\\tPL:ILLUMINA\\tSM:{Name}' {Ref} {Path}/{LeftFile} {Path}/{RightFile} |{Picard} SortSam INPUT=/dev/stdin OUTPUT={Output}/{Name}.sort.bam SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT\n"
def MarkDuplicates(Path,Name):
    return f"{Picard} MarkDuplicates INPUT={Path}/{Name}.sort.bam OUTPUT={Path}/{Name}.sort.dedup.bam METRICS_FILE={Path}/{Name}_dedup REMOVE_DUPLICATES=true CREATE_INDEX=true ASSUME_SORTED=true VALIDATION_STRINGENCY=LENIENT MAX_FILE_HANDLES=2000\n"
def MergeSamFiles(Path,BamList,Name):
    Command = f"{Picard} MergeSamFiles"
    for bam in BamList: Command += f" I={Path}/{bam}.sort.bam"
    Command += f" SORT_ORDER=coordinate O={Path}/{Name}_tmp.bam AS=true\n"
    return Command
def AddOrReplaceReadGroups(InBam,Ref,Output,Name):
    if InBam.endswith('cram'):
        return f"{Samtools} view -bS {InBam}|{Samtools} sort --reference {Ref} -T {Output}/{Name} --output-fmt BAM - |{Picard} AddOrReplaceReadGroups INPUT=/dev/stdin O={Output}/{Name}.sort.bam SO=coordinate ID={Name} LB={Name} PL=illumina PU={Name} SM={Name} CREATE_INDEX=true VALIDATION_STRINGENCY=LENIENT\n"
    else:
        return f"{Picard} AddOrReplaceReadGroups I={InBam} O={Output}/{Name}.sort.bam SO=coordinate ID={Name} LB={Name} PL=illumina PU={Name} SM={Name} CREATE_INDEX=true VALIDATION_STRINGENCY=LENIENT\n"
def RemoveList(Path,BamList,Name):
    Command = ''
    if len(BamList) > 1:
        for Bam in BamList: Command += f'rm {Path}/{Bam}.sam\nrm {Path}/{Bam}.sort.bam\n'
        Command += f'rm {Path}/{Name}_dedup\nrm {Path}/{Name}_tmp.bam\nrm {Path}/{Name}.sort.bai\nrm {Path}/{Name}.sort.bam\n'
    else: Command += f'rm {Path}/{Name}_dedup\nrm {Path}/{Name}.sam\nrm {Path}/{Name}.sort.bam\n'
    return Command
@click.command()
@click.option('-i','--input',type=click.File('r'),help='The input file',required=True)
@click.option('-r','--ref',type=str,help='The reference file')
@click.option('-o','--output',type=str,help='The output file path',default='.')
@click.option('-s','--output1',type=str,help='The shell  path',default='.')
def main(input,ref,output,output1):
    '''
    /xxx/xxx/xxx/xxx.bam    IROO-ORI10
    '''
    if output1[-1] == '/': output1 = output1[:-1]
    if not os.path.exists(f'{output1}/shell/shell2/shell3'): os.system(f'mkdir -p  {output1}/shell/shell2/shell3')
    #OUTPUT = open(f'{output1}/shell/{}.mapping.sh','w')
    
    for line in input:
        line = line.strip().split()
        OUTPUT = open(f'{output1}/shell/shell2/shell3/{line[1]}.rename.markdup.new.sh','w')
        #OUTPUT.write(AddOrReplaceReadGroups(line[0],ref,output,line[1]))
        #OUTPUT.write(f"echo {line[1]} merge finished!\n")
        OUTPUT.write(MarkDuplicates(output,line[1]))
        OUTPUT.write(f"echo {line[1]} remove dup finished!\n\n")
        os.system(f'chmod 755 {output1}/shell/shell2/shell3/{line[1]}.rename.markdup.new.sh')
if __name__ == '__main__':
    main()
