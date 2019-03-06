# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Wed Jul 25 15:34:13 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''
# You should run 'qualimap bamqc' first. qualimap bamqc -bam {Bam} -outdir {output} -outformat HTML --java-mem-size={memory}G
import sys,os,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

@click.command()
@click.option('-i','--filelist',type=click.File('r'),help='the result dir list of qualimap',required=True)
@click.option('-f','--faidx',type=click.File('r'),help='The faidx file of the reference genome',required=True)
@click.option('-1','--chr1-id',type=str,help='The name of Chromosome 1 in the reference genome',default='1')
@click.option('-x','--chrx-id',type=str,help='The name of Chromosome X in the reference genome',default='X')
@click.option('-o','--output',type=click.File('w'),help='The output file',default='Gender.info')
def main(filelist,faidx,chr1_id,chrx_id,output):
    '''
    need .fai file. you can get the file using: samtools faidx ref.fa
    1       275406953       3       80      81
    2       248966461       278849546       80      81
    3       223996068       530928091       80      81
    '''
    StartPos = 0
    for line in faidx:
        line = line.strip().split()
        if line[0] == chr1_id: Chr1Pos = [StartPos,StartPos+int(line[1])]
        elif line[0] == chrx_id: ChrXPos = [StartPos,StartPos+int(line[1])]
        StartPos += int(line[1])
    output.write(f'FileName\tChr1MeanCover\tChrXMeanCover\tRatio\tGender\n')
    for dir in filelist:
        dir = dir.strip()
        if dir[-1] == '/' : dir = path[:-1]
        FileName = dir.split('/')[-1]
        CoverFile = open(f'{dir}/raw_data_qualimapReport/coverage_across_reference.txt','r')
        Chr1CoverList, ChrXCoverList = [], []
        for line in CoverFile:
            if line.startswith('#'):continue
            line = line.strip().split()
            if Chr1Pos[0] <= round(float(line[0])) <= Chr1Pos[1]:
                Chr1CoverList.append(float(line[1]))
            elif ChrXPos[0] <= round(float(line[0])) <= ChrXPos[1]:
                ChrXCoverList.append(float(line[1]))
        if len(Chr1CoverList) == 0: Chr1MeanCover = 0
        else: Chr1MeanCover = round(sum(Chr1CoverList)/len(Chr1CoverList),2)
        if len(ChrXCoverList) == 0: ChrXMeanCover = 0
        else:ChrXMeanCover = round(sum(ChrXCoverList)/len(ChrXCoverList),2)
        if Chr1MeanCover == 0: Ratio = 0
        else: Ratio = round(ChrXMeanCover/Chr1MeanCover,6)
        Gender = 'Male'
        if Ratio > 0.75: Gender = 'Female'
        output.write(f'{FileName}\t{Chr1MeanCover}\t{ChrXMeanCover}\t{Ratio}\t{Gender}\n')
if __name__ == '__main__':
    main()
