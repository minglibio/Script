########################### Fst ########################
rm(list=ls())
args<-commandArgs(TRUE)
FST<-args[1]
OutName<-args[2]
source("~/script/Selection/Fst/FST.source.r")

mydata=read.table(FST, header=T)      ##Input File Name
head(mydata)
mydata=mydata[order(as.numeric(mydata[,1]),decreasing = FALSE),]
colnames(mydata)=c("CHR","BP","FST")
dim(mydata)
mydata[1:10,]
GAPIT.Manhattan(mydata,name.of.trait=OutName)       ##Output File Name
