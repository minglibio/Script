# -*- coding: utf-8 -*- 
import sys
if sys.getdefaultencoding() != 'utf-8': 
	reload(sys) 
sys.setdefaultencoding('utf-8')
import os
import numpy as np
import click
import types 

def form_bed(in_file1): #读取原始的bed文件
	Chr = {}
	Novel ={}
	tmp = "less -S  %s" %(in_file1)
	for line in os.popen(tmp):
		line = line.strip().split()
                #if len(line[0])<3:
		if len(line[0].split("_"))==1:
			Chr[int(line[3])] = "\t".join([line[0],line[1],line[2]])
		else:
			Novel.setdefault(line[0],[]).append(line[3])
	return (Chr,Novel)
def form_matrix(infile2): #读取矩阵matrix文件
	matrix={}
	with open(infile2, 'r') as f:
		for line in f:
			line = line.strip().split()
			if int(line[0])!=int(line[1]):
				matrix.setdefault(line[1],[]).append([int(line[0]),int(line[2])])
			else:
				pass
	return matrix

def produce_Mmax(x):
	if np.array(x).size>2:
		x1=np.delete(x, np.where(x==np.max(x,axis=0))[0][0], 0).tolist()
		number=np.array(x1).max(axis=0)
		if number[1]>=3:
			return x1[np.where(x1==np.max(x1,axis=0))[0][0]][0]
		else:
			return  "link<3"
	else:
		return "none array"
def find_position(key1,matrix,Chr):#迭代寻找novel在常染色体上的位置,递归大法好，但一定要注意数据类型 type()
	
	if  key1  in matrix:
		#print str(886)+"\t"+str(type(key1))
		x=np.array(matrix[key1])
		#print str(886)+"\t"+str(key1)+"\t"+str(x)
		if np.array(x).size>=2:
			number=np.array(matrix[key1]).max(axis=0)
			if number[1]>=3:
				index= x[np.where(x==np.max(x,axis=0))[0][0]][0] 
				#print str(key1)+"\t"+str(Chr[int(index)])
				if index  in Chr:
					#print index,Chr[index]
					b=Chr[index]
					return  "Once:" + str(key1)+"\t"+str(b)
				else:
					#link-----link-----link模式的递归处理
					key=str(index)
					#link-----link 间的值的次高递归处理
					#x1=np.delete(x, np.where(x==np.max(x,axis=0))[0][0], 0).tolist()
					key2=produce_Mmax(x)
					#print  x[np.where(x==np.max(x,axis=0))[0][0]:, :]
					#return "link-link" + str(key1)+"\t"+str(find_position(key2,matrix,Chr))+"NNNNNN"
					return "link-link2:" + str(key1)+"\t"+str(find_position(str(key2),matrix,Chr)) +"NNNNNN"+"link-link-link3:" + str(key1)+"\t"+str(find_position(key,matrix,Chr))
	
			else:
				return  "link<3"
		else:
			return  "array none"
			
	else:
		pass
		return "PASS"

@click.command()
@click.option('--bed', help='输入Hic产生的bed文件')
@click.option('--matrix', help='输入Hic产生的matrix文件')
@click.option('--output', help='输出文件及路径')

def main(bed,matrix,output):
	(Chr,Novel)=form_bed(bed)
	matrix=form_matrix(matrix)
	#for key in matrix:
	#	print  str(key)+str(matrix[key])
	for key in Novel:
		#key1=np.array(Novel[key]).max(axis=1)
		key1=max(Novel[key])
		position=find_position(key1,matrix,Chr)
		#print str(key)+"\t"+str(position)
		with open(output, 'a') as f:
			f.write(str(key)+"NNNNNN"+"\t"+str(position)+'\n')
if __name__ == '__main__':
	 main()
