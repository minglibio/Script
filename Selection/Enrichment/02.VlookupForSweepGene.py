# -*- coding: utf-8 -*-
#!/usr/bin/env python3
'''
Created on Wed Aug 22 16:03:13 CST 2018
@Mail: minnglee@163.com
@Author: Ming Li
'''

import sys,os,logging,click,re

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadGeneList(file):
    '''
    #!Original data download from ftp://ftp.ncbi.nih.gov/genomes/Anas_platyrhynchos/GFF/, liftOver by zhouzhengkui@caas.cn
    chr1	RefSeq	region	1	600996	.	-	.	ID=id156040;Dbxref=taxon:8839;Name=Unknown;breed=Pekin duck;chromosome=Unknown;country=
    chr1	Gnomon	gene	4877	11173	.	-	.	ID=gene6838;Dbxref=GeneID:101794669;Name=LOC101794669;gbkey=Gene;gene=LOC101794669;gene
    chr1	Gnomon	mRNA	4877	11173	.	-	.	ID=rna13680;Parent=gene6838;Dbxref=GeneID:101794669,Genbank:XM_005016073.2;Name=XM_0
    chr1	Gnomon	exon	4877	5478	.	-	.	ID=id156271;Parent=rna13680;Dbxref=GeneID:101794669,Genbank:XM_005016073.2;gbkey=mRNA;gene=LOC1017
    chr1	Gnomon	CDS	5351	5478	.	-	2	ID=cds9951;Parent=rna13680;Dbxref=GeneID:101794669,Genbank:XP_005016130.1;Name=XP_0050
    '''
    GeneDict = {}
    for line in file:
        if line.startswith('#'):continue
        line = line.strip().split('\t')
        if line[2] == 'gene':
            GeneName = re.search('(?<=Name=).*?(?=;)',line[8]).group()
            CHR = line[0].replace('chr','')
            GeneDict.setdefault(CHR,[]).append([int(line[3]),int(line[4]),GeneName])
    return GeneDict
@click.command()
@click.option('-g','--gtf',type=click.File('r'),help='The GTF/GFF file',required=True)
@click.option('-b','--bed',type=click.File('r'),help='The bed file',required=True)
@click.option('--updown',type=int,help='enlarge region',default=0)
@click.option('-o','--output',type=str,help='The output file',required=True)
def main(gtf,bed,updown,output):
    GeneDict = LoadGeneList(gtf)
    GeneSet = set()
    RegionGeneOut = open(f'{output}.gene', 'w')
    GeneListOut = open(f'{output}.genelist', 'w')
    for line in bed:
        GeneList = []
        line = line.strip().split()
        CHR = line[0].replace('chr','')
        for gene in GeneDict[CHR]:
            if int(line[1])-updown < gene[0] < int(line[2])+updown:
                GeneList.append(gene[2])
                GeneSet.add(gene[2])
            elif int(line[1])-updown < gene[1] < int(line[2])+updown:
                GeneList.append(gene[2])
                GeneSet.add(gene[2])
            elif gene[0] <= int(line[1])-updown < int(line[2])+updown <= gene[1]:
                GeneList.append(gene[2])
                GeneSet.add(gene[2])
            elif gene[0] > int(line[2])+updown:
                break
        RegionGeneOut.write('{0}\t{1}\n'.format('\t'.join(line),'\t'.join(GeneList)))
    for gene in GeneSet:
        GeneListOut.write(f'{gene}\n')
if __name__ == '__main__':
    main()
