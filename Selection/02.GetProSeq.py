# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Mon Jul 31 10:24:35 2017
@Mail: minnglee@163.com
@Author: Ming Li
"""

import sys,os,logging,click
import re

logging.basicConfig(filename=os.path.basename(__file__).replace('.py','.log'),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

def LoadProSeq(file):
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
    File = os.popen(f'less {file}')
    Dict = {}
    seq = ''
    flag = 0
    for line in File:
        line = line.strip()
        if line.startswith('/gene='):
            GeneName = re.search('(?<=/gene=").*?(?=")',line).group()
        elif line.startswith('ORIGIN') : flag = 1
        elif flag == 1 and not line.startswith('//'):
            line = line.split()
            seq += ''.join(line[1:])
        elif line.startswith('//'):
            if not GeneName in Dict : Dict[GeneName] = seq
            elif len(Dict[GeneName]) < len(seq) : Dict[GeneName] = seq
            seq = ''
            flag = 0
    return Dict
@click.command()
@click.option('-p','--ProSeq',type=str,help='Protein Sequence file [*.gbk.gz]',required=True)
@click.option('-g','--GeneList',type=click.File('r'),help='Gene List file',required=True)
@click.option('-o','--output',type=click.File('w'),help='The output file',required=True)
def main(proseq,genelist,output):
    ProSeq = LoadProSeq(proseq)
    for gene in genelist:
        gene = gene.strip()
        if not gene in ProSeq:continue
        output.write(f'>{gene}\n{ProSeq[gene].upper()}\n')
if __name__ == '__main__':
    main()
