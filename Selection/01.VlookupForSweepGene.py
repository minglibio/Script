# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Wed Jun 14 21:47:43 2017
@Mail: minnglee@163.com
@Author: Ming Li
"""

import sys,os,re,logging,click

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadGeneList(File):
    '''
    #!Original data download from ftp://ftp.ncbi.nih.gov/genomes/Anas_platyrhynchos/GFF/, liftOver by zhouzhengkui@caas.cn
    chr1	RefSeq	region	1	600996	.	-	.	ID=id156040;Dbxref=taxon:8839;Name=Unknown;breed=Pekin duck;chromosome=Unknown;country=China: Beijing;gbkey=Src;genome=genomic;isolation-source=Gold Star Duck Production;mol_type=genomic DNA;sex=female
    chr1	Gnomon	gene	4877	11173	.	-	.	ID=gene6838;Dbxref=GeneID:101794669;Name=LOC101794669;gbkey=Gene;gene=LOC101794669;gene_biotype=protein_coding
    chr1	Gnomon	mRNA	4877	11173	.	-	.	ID=rna13680;Parent=gene6838;Dbxref=GeneID:101794669,Genbank:XM_005016073.2;Name=XM_005016073.2;gbkey=mRNA;gene=LOC101794669;product=guanylyl cyclase-activating protein 1;transcript_id=XM_005016073.2
    chr1	Gnomon	exon	4877	5478	.	-	.	ID=id156271;Parent=rna13680;Dbxref=GeneID:101794669,Genbank:XM_005016073.2;gbkey=mRNA;gene=LOC101794669;product=guanylyl cyclase-activating protein 1;transcript_id=XM_005016073.2
    chr1	Gnomon	CDS	5351	5478	.	-	2	ID=cds9951;Parent=rna13680;Dbxref=GeneID:101794669,Genbank:XP_005016130.1;Name=XP_005016130.1;gbkey=CDS;gene=LOC101794669;product=guanylyl cyclase-activating protein 1;protein_id=XP_005016130.1
    '''
    GeneDict = {}
    CDSDict = {}
    for line in File:
        if line.startswith('#'):continue
        line = line.strip().split('\t')
        if line[2] == 'gene':
            GeneName = re.search('(?<=Name=).*?(?=;)',line[8]).group()
            CHR = line[0].replace('chr','')
            GeneDict.setdefault(CHR,[]).append([int(line[3]),int(line[4]),GeneName])
    return GeneDict
@click.command()
@click.option('--updown',help='enlarge region',type=int,default=0)
@click.option('-g','--gtf',help='GTF file',type=click.File('r'),required=True)
@click.option('-b','--bed',help='Bed file',type=click.File('r'),required=True)
@click.option('-o','--output',help='Output file',type=str,required=True)
def main(updown,gtf,bed,output):
    GeneDict = LoadGeneList(gtf)
    GeneSet = set()
    RegionGeneOut = open(f'{output}.gene', 'w')
    GeneListOut = open(f'{output}.genelist', 'w')
    for line in bed:
        GeneList = []
        line = line.strip().split()
        CHR = line[0].replace('chr','')
        for gene in GeneDict[CHR]:
            if int(line[1]) - updown < gene[0] < int(line[2]) + updown:
                GeneList.append(gene[2])
                GeneSet.add(gene[2])
            elif int(line[1]) - updown < gene[1] < int(line[2]) + updown:
                GeneList.append(gene[2])
                GeneSet.add(gene[2])
            elif gene[0] <= int(line[1]) - updown < int(line[2]) + updown <= gene[1]:
                GeneList.append(gene[2])
                GeneSet.add(gene[2])
            elif gene[0] > int(line[2]) + updown:
                break
        Pos = '\t'.join(line)
        RegionGeneList = '\t'.join(GeneList)
        RegionGeneOut.write(f'{Pos}\t{RegionGeneList}\n')
    for gene in GeneSet:
        GeneListOut.write(f'{gene}\n')
if __name__ == '__main__':
    main()
