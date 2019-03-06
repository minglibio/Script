source("~/script/GWAS/MANHATTAN_QQ_FDR.r")
setwd("./")

args<-commandArgs(TRUE)
IN<-args[1]
name<-args[2]

mydata=read.table(IN, header=TRUE)
mydata[,3] = p.adjust(mydata[,3],method="fdr",n=length(mydata[,3]))
GAPIT.Manhattan(mydata,name.of.trait=paste("",name,sep =""))
mydata=mydata[order(as.numeric(mydata[,3]),decreasing = FALSE),]
myoutdata=mydata[1:2001,]
myoutdata[,3] <-  -log10(myoutdata[,3])
write.table(myoutdata,file=paste("gwas.fdr.",name,".assoc.t2000.txt",sep =""), col.names=T, row.names=F, quote=F,sep=" ")

