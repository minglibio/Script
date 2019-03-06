# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Mon Jul 31 10:24:35 2017
@Mail: minnglee@163.com
@Author: Ming Li
"""

import sys
import os
import argparse
import time
import re
import gzip

def GetCommandLine():
    CommandLine = 'python3 {0}'.format(' '.join(sys.argv))
    return(CommandLine)
LogFile = None
def log(LogInfo):
    '''
    Output the LogInfo to log file
    '''
    global LogFile
    if sys.platform == 'linux':
        CurrentFolder = os.getcwd()
        LogFileName = re.split('/|\\\\',sys.argv[0].strip())
        LogFileName = LogFileName[-1].split('.')
        LogFileName = '{0}/{1}.log'.format(CurrentFolder,LogFileName[0])
        if LogFile: LogFile.write(LogInfo+'\n')
        else:
            LogFile = open(LogFileName,'w')
            LogFile.write(LogInfo+'\n')
    else:
        print(LogInfo)
def LoadProSeq():
    '''
LOCUS       XP_012948003             592 aa            linear   VRT 24-MAY-2017
DEFINITION  tyrosine-protein phosphatase non-receptor type 11-like [Anas
            platyrhynchos].
ACCESSION   XP_012948003
VERSION     XP_012948003.1
DBLINK      BioProject: PRJNA208071
DBSOURCE    REFSEQ: accession XM_013092549.2
KEYWORDS    RefSeq.
SOURCE      Anas platyrhynchos (mallard)
  ORGANISM  Anas platyrhynchos
            Eukaryota; Metazoa; Chordata; Craniata; Vertebrata; Euteleostomi;
            Archosauria; Dinosauria; Saurischia; Theropoda; Coelurosauria;
            Aves; Neognathae; Anseriformes; Anatidae; Anas.
COMMENT     MODEL REFSEQ:  This record is predicted by automated computational
            analysis. This record is derived from a genomic sequence
            (NW_004676297.1) annotated using gene prediction method: Gnomon.
            Also see:
                Documentation of NCBI's Annotation Process
            
            ##Genome-Annotation-Data-START##
            Annotation Provider         :: NCBI
            Annotation Status           :: Full annotation
            Annotation Version          :: Anas platyrhynchos Annotation
                                           Release 102
            Annotation Pipeline         :: NCBI eukaryotic genome annotation
                                           pipeline
            Annotation Software Version :: 7.4
            Annotation Method           :: Best-placed RefSeq; Gnomon
            Features Annotated          :: Gene; mRNA; CDS; ncRNA
            ##Genome-Annotation-Data-END##
            COMPLETENESS: full length.
FEATURES             Location/Qualifiers
     source          1..592
                     /organism="Anas platyrhynchos"
                     /isolation_source="Gold Star Duck Production"
                     /db_xref="taxon:8839"
                     /chromosome="Unknown"
                     /sex="female"
                     /country="China: Beijing"
                     /breed="Pekin duck"
     Protein         1..592
                     /product="tyrosine-protein phosphatase non-receptor type
                     11-like"
                     /calculated_mol_wt=67909
     CDS             1..592
                     /gene="LOC101789439"
                     /coded_by="XM_013092549.2:147..1925"
                     /db_xref="GeneID:101789439"
ORIGIN      
        1 mvrwfhpnis gieaeklllt rgvhgsflar psksnpgdft lsvrrndevt hikiqntgdy
       61 ydlyggekfa tlaelvqyyt eqqgllrekn snvielkypl ncqdptserw yhghltgkea
      121 eklltekgkp gsflvresqs kpgdfvlsvl tnedkmetgd rkphvthvmi hyqpdgkydv
      181 gggerfdtlt dlvehykknp mveksgavvh lkqpfnatri naanienrvk elnkmadhse
      241 kakqgfweef emlqqqeckl lyprkegqrp enkaknrykn ilpfdttrva lrdvdesvpg
      301 sdyinanyik sipedgrnse hckiyiatqg clqttvndfw tmvyqenshv ivmttkever
      361 grnkcfrywp dkgcakeygc icvrnvsere aqgyylrele itrtdrderp rvvkhyqyfs
      421 wpdhgvpnep ggvlsfldqv nraqrsipdt gpiivhcsag igrtgtiivi dilvdiihrq
      481 gldcdidipk tiqmvrrqrs gmvqteaqyk fvymavqqfi eaeqkrleee qrnkrkerdy
      541 lnigyspmek grakgqppsp raqsvvddes asvyenlnik spkvsgmsnt gr
//
    '''
    Dict={}
    seq=''
    flag = 0
    GzFile = False
    if args.GzFile:
        ProSeq = gzip.open(args.ProSeq,'rb')
        GzFile = True
    else: 
        ProSeq = open(args.ProSeq)
    for line in ProSeq:
        if GzFile: line = line.decode('GBK')
        line = line.strip()
        if line.startswith('/gene='):
            GeneName = re.search('(?<=/gene=").*(?=")',line).group()
#            print(GeneName)
        elif line.startswith('ORIGIN'):
            flag = 1
        elif flag == 1 and not line.startswith('//'):
            line = line.split()
            seq += ''.join(line[1:])
        elif line.startswith('//'):
            if not GeneName in Dict:
                Dict[GeneName] = seq
            elif len(Dict[GeneName]) < len(seq):
                Dict[GeneName] = seq
            seq=''
            flag = 0
    return Dict
def GetProSeq():
    ProSeq = LoadProSeq()
    for gene in args.GeneList:
        gene = gene.strip()
        if not gene in ProSeq:continue
        args.output.write('>{0}\n{1}\n'.format(gene,ProSeq[gene].upper()))
def main():
    print('Running...')
    log('The start time: {0}'.format(time.ctime()))
    log('The command line is:\n{0}'.format(GetCommandLine()))
    GetProSeq()
    log('The end time: {0}'.format(time.ctime()))
    print('Done!')
#############################Argument
parser = argparse.ArgumentParser(description=print(__doc__),formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-p','--ProSeq',metavar='File',dest='ProSeq',help='Protein Sequence file [gbk]',type=str,required=True)
parser.add_argument('-g','--GeneList',metavar='File',dest='GeneList',help='Gene List file',type=open,required=True)
parser.add_argument('-G','--GzFile',dest='GzFile',help='The input is gz file',action='store_true',default=True)
parser.add_argument('-o','--Output',metavar='File',dest='output',help='Output file',type=argparse.FileType('w'),required=True)
args = parser.parse_args()
###########################
if __name__ == '__main__':
    main()