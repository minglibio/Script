# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Fri Apr 13 19:06:43 2018
@Mail: minnglee@163.com
@Author: Ming Li
"""

import sys,os,argparse,time,re
import gzip 
import msprime
from math import exp

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
def SimulationUsingMsprime(iterate):
    nhafr = 200 # num. sampled African haplotypes 
    nheur = 8000 # num. sampled European haplotypes 
    nhnea = 200 # num. sampled Neand. haplotypes 
    nbp = 10000000 # simulated 10 Mb 
    rho = 1.0e-8 # recombination rate 
    mu = 1.2e-8 # mutation rate of base simulation (can downsample to mu = 1.2e-8 for analysis) 
 
    seed = iterate # we used seeds 1-100 
#    outprefix = args.output # output file prefix  
 
    NNE = 1500 # Neandertal effective size 
    NA = 15000 # Ancestral African eff. size 
    NOoA = 2000 # Out-of-African eff. size 
    r = .02 # growth rate since agriculture 
 
    # times are in generations before present 
    TNeand = 16000 # neandertal-human split time 
    TOoA = 2400 # time of Out of Africa event 
    Tintrostart = 2000 # start of introgression 
    Tintroend = Tintrostart-20 # end introgression 
    Tgrowth = 200 # time of recent growth  
 
    # migration rates are proportion of population made of new immigrants each generation 
    mAFEU = 1.0e-5 # mig. rate betw. Afr. and Eur. 
    mintro = 0.0015 # introgression from Neandertal into Europe 
 
    NEUnow = NOoA*exp(Tgrowth*r)  
    NAFnow = NA*exp(Tgrowth*r) 
 
    pop_config = [ 
            msprime.PopulationConfiguration(sample_size = None, initial_size = NAFnow,growth_rate = r), 
            msprime.PopulationConfiguration(sample_size = None, initial_size = NEUnow, growth_rate = r), 
            msprime.PopulationConfiguration(sample_size = None, initial_size = NNE)] 
 
    samples = [msprime.Sample(0,0) for i in range(nhafr)] + [msprime.Sample(1,0) for i in range(nheur)] + [msprime.Sample(2,Tintrostart) for i in range(nhnea)] # Neand. haplotypes sampled 2000 gen. ago  
 
    # migration between Africa and Europe 
    mig_mat = [[0,mAFEU,0],[mAFEU,0,0],[0,0,0]] 
 
    # onset of growth with agriculture 
    growth_event = [msprime.PopulationParametersChange(time = Tgrowth, growth_rate = 0.0)] 
 
    # neanderthal introgression 
    intro_event = [msprime.MigrationRateChange(time = Tintroend, rate = mintro, matrix_index = (1,2)), 
                   msprime.MigrationRateChange(time = Tintrostart, rate = 0, matrix_index = (1,2))] 
 
    # human out of Africa 
    ooa_event = [msprime.MigrationRateChange(time=TOoA-.01, rate=0), msprime.MassMigration(time=TOoA, 
                 source=1, destination=0)] 
 
    # Neanderthal out of Africa 
    neand_event = [msprime.MassMigration(time=TNeand, source=2, destination=0)] 
 
    events = growth_event + intro_event + ooa_event + neand_event 
    
    
    # Use the demography debugger to print out the demographic history
    # that we have just described.
    dd = msprime.DemographyDebugger(
        population_configurations=pop_config,
        migration_matrix=mig_mat,
        demographic_events=events)
    dd.print_history()
    '''
    # make the simulation 
    treeseq = msprime.simulate(population_configurations = pop_config, samples = samples, 
                               migration_matrix = mig_mat, demographic_events = events, length = nbp, recombination_rate = 
                               rho,mutation_rate = mu, random_seed = seed)
    # output the vcf 
#    with gzip.open(outprefix+".vcf.gz","wb") as vcffile: 
#        treeseq.write_vcf(vcffile,2)
#    vcffile = gzip.open('{0}.vcf.gz'.format(outprefix),"w")
    vcffile = open('{0}.i{1}.vcf'.format(outprefix,iterate),"w")
    treeseq.write_vcf(vcffile,2)
    os.system('gzip {0}.i{1}.vcf'.format(outprefix,iterate))
 
    # determine intro. status for Eur. hapl. 
    def node_get_pop(tree,node,admix_time, split_time): 
        # if the time of a node is < admix_time, its population is found by tracing up the tree 
        while tree.get_time(node) <= admix_time: 
            node = tree.get_parent(node) 
        # if the time of the parent node is > split_time, the returned pop. is -1 (unknown)  
        if tree.get_time(node) > split_time: 
            return -1 
        else: return tree.get_population(node) 
 
    introfile = open('{0}.i{1}.intro'.format(outprefix,iterate),"w") 
    eurohaps = range(nhafr,nhafr+nheur) 
    for tree in treeseq.trees(): 
        introgressed = [x for x in eurohaps if node_get_pop(tree,x,Tintrostart,TNeand)==2] 
        if len(introgressed)>0: 
            start,stop=tree.get_interval() 
            introfile.write('{0}\t{1}\t'.format(round(start,1),round(stop,1)))
            for x in introgressed:
                introfile.write('{0}\t'.format(x))
            introfile.write('\n')
    '''
def Running():
    SimulationUsingMsprime(args.seed) 
def main():
    print('Running...')
    log('The start time: {0}'.format(time.ctime()))
    log('The command line is:\n{0}'.format(GetCommandLine()))
    Running()
    log('The end time: {0}'.format(time.ctime()))
    print('Done!')
#############################Argument
parser=argparse.ArgumentParser(description=print(__doc__),formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-s','--seed',metavar='Ind',dest='seed',help='The number of seed (we used seeds 1-100; default:50)',type=int,default=100)
#parser.add_argument('-o','--Output',metavar='File',dest='output',help='The prefix of output file',type=str,required=True)
args=parser.parse_args()
###########################
if __name__=='__main__':
    main()
