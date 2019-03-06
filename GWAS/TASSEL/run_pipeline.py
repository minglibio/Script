#!/usr/bin/env python3

'''
------------------------------------------------------------------------------------------
Author: Ming Li
Email: minnglee@163.com
Time: 2016/8/8
Version: 1.0
------------------------------------------------------------------------------------------
'''

import sys
import getopt
import os
import time
import re

def usage():
    print(__doc__)
    print('''Usage: python script.py [option] [parameter]
    -m/--min_memory             the java min memory (default: -Xms512m)
    -M/--max_memory             the java max memory (default: -Xmx1536m)
    -c/---configFile            the config file
    -h/--help                   show possible options
------------------------------------------------------------------------------------------''')

def main():
    LIB=os.listdir(TASSEL_path+'lib')
    PATH_LIB=[]
    for lib in LIB:
        if re.match('\.jar$',lib):
            PATH_LIB.append(TASSEL_path+'lib/'+lib)
    PATH_LIB.append(TASSEL_path+'sTASSEL.jar')
    CP=':'.join(PATH_LIB)
    log_file.write('CP: '+CP+'\n')
    os.system('/home/share/software/jre1.8.0_25/bin/java -classpath '+CP+' '+java_min_memory+' '+java_max_memory+' net.maizegenetics.pipeline.TasselPipeline '+configFile)
#############################default
java_min_memory = '-Xms512m'
java_max_memory = '-Xmx1536m'
TASSEL_path='/home/yjiang/liming/KIZ_WMS_GAnoout_vcf/gwas/GLM/TASSEL_5/'
#############################
opts,argvs=getopt.getopt(sys.argv[1:],'hm:M:c:',['help','min_memory=','max_memory=','configFile='])
for op,value in opts:
    if op=='-m' or op=='--min_memory':
        java_min_memory=value
    elif op=='-M' or op=='--max_memory':
        java_max_memory=value
    elif op=='-c' or op=='--configFile':
        configFile=[value]
    elif op=='-h' or op=='--help':
        usage()
        sys.exit(1)
if len(sys.argv) == 1:
    usage()
    sys.exit(1)
##########################
CurrentFolder=os.getcwd()
log_file=open(CurrentFolder+'/run_pipeline.log','w')
###########################
if __name__=='__main__':
    log_file.write('The start time: '+time.ctime()+'\n')
    log_file.write('Min Memory Settings: '+java_min_memory+'\n')
    log_file.write('Max Memory Settings: '+java_max_memory+'\n')
    log_file.write('Tassel Pipeline Arguments: '+str(configFile)+'\n')
    main()
    log_file.write('The end time: '+time.ctime()+'\n')
