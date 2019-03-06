`GAPIT.Pruning` <-
function(values,DPP=5000000){
#Object: To get index of subset that evenly distribute
#Output: Index
#Authors: Zhiwu Zhang  ## edit by zhkzhou@126.com 
# Last update: May 28, 2011
##############################################################################################

#No change if below the requirement
if(length(values)<=DPP)return(c(1:length(values)))

#values= log.P.values

values=sqrt(values)  #This shift the weight a little bit to the low building.
theMin=min(values)
theMax=max(values)
range=theMax-theMin
interval=range/DPP

ladder=round(values/interval)
ladder2=c(ladder[-1],0)
keep=ladder-ladder2
index=which(keep>0)

return(index)
}#end of GAPIT.Pruning



`GAPIT.Manhattan` <-
function(GI.MP = NULL, name.of.trait = "Trait",plot.type = "Genomewise", plot.type2 = "Chromosomewise",
DPP=5000000,cutOff=0.01,band=5,seqQTN=NULL){
#Object: Make a Manhattan Plot
#Options for plot.type = "Separate_Graph_for_Each_Chromosome" and "Same_Graph_for_Each_Chromosome"
#Input GI.MP-three columns: choromosome, bp and p
#Output: A pdf of the Manhattan Plot
#Authors: Alex Lipka, Zhiwu Zhang, and Meng Li      ## edit by zhkzhou@126.com 
# Last update: May 10, 2011
##############################################################################################

#if(name.of.trait=="Fst Mal VS Ind Win40K_40"){Threshold=0.265146}
#if(name.of.trait=="Fst Ind VS Pek Win40K_40"){Threshold=0.372253}
#if(name.of.trait=="Fst Mal VS Pek Win40K_40"){Threshold=0.369643}

if(is.null(GI.MP)) return

borrowSlot=4
GI.MP[,borrowSlot]=0 #Inicial as 0
if(!is.null(seqQTN))GI.MP[seqQTN,borrowSlot]=1

#Eeep QTN with NA p values (set it to 1)
index=which(GI.MP[,borrowSlot]==1  & is.na(GI.MP[,3]))
GI.MP[index,3]=1

GI.MP=matrix(as.numeric(as.matrix(GI.MP) ) ,nrow(GI.MP),ncol(GI.MP))

#Remove all SNPs that do not have a choromosome, bp position and p value(NA)
GI.MP <- GI.MP[!is.na(GI.MP[,1]),]
GI.MP <- GI.MP[!is.na(GI.MP[,2]),]
GI.MP <- GI.MP[!is.na(GI.MP[,3]),]

#Remove all SNPs that have P values between 0 and 1 (not na etc)
#GI.MP <- GI.MP[GI.MP[,3]>0,]
#GI.MP <- GI.MP[GI.MP[,3]<=1,]

#Remove chr 0 and 99
GI.MP <- GI.MP[GI.MP[,1]!=0,]

numMarker=nrow(GI.MP)
bonferroniCutOff=-log10(cutOff/numMarker)

#Replace P the -log10 of the P-values
#GI.MP[,3] <-  -log10(GI.MP[,3])

#y.lim <- ceiling(max(GI.MP[,3]))
#y.lim = 0.2
#print("The max -logP vlaue is")
#print(y.lim)

chm.to.analyze <- unique(GI.MP[,1])

chm.to.analyze=chm.to.analyze[order(chm.to.analyze)]
numCHR= length(chm.to.analyze)

#Chromosomewise plot
if(plot.type2 == "Chromosomewise")
{
#print("Manhattan ploting Chromosomewise")

  pdf(paste("ZFst.", name.of.trait,".Chromosomewise.pdf" ,sep = ""), width = 10)
  par(mar = c(5,5,4,3), lab = c(8,5,7))
  for(i in 1:numCHR)
  {
    #Extract SBP on this chromosome
    subset=GI.MP[GI.MP[,1]==chm.to.analyze[i],]

  	y.lim <- ceiling(max(subset[,3]))  #set upper for each chr
  	#y.lim=0.2  #set upper for each chr
  	if(length(subset)>3){
      x <- as.numeric(subset[,2])/10^(6)
      y <- as.numeric(subset[,3])
    }else{
      x <- as.numeric(subset[2])/10^(6)
      y <- as.numeric(subset[3])
    }

  	#Prune most non important SNPs off the plots
    order=order(y,decreasing = TRUE)
    y=y[order]
    x=x[order]

    index=GAPIT.Pruning(y,DPP=round(DPP/numCHR))
   	x=x[index]
  	y=y[index]

    #color.vector <- subset(temp.par.data[,7], temp.par.data[,4] == i)
    plot(y~x,type="p", ylim=c(0,y.lim), xlim = c(min(x), max(x)), col = "navy", xlab = expression(Base~Pairs~(x10^-6)), 
    ylab = "ZFst", main = paste("Chromosome",chm.to.analyze[i],sep=" "),cex.lab=1 , pch=20, xaxs="i", yaxs="i" )
#abline(h=bonferroniCutOff,col="forestgreen")
#abline(h = Threshold, col="dimgray", lty=2, lwd=0.5)
  	##print("manhattan plot (chr) finished")
  }
  print("Manhattan-Plot.Chromosomewise finished!")
  dev.off()
  #print("manhattan plot on chromosome finished")
} #Chromosomewise plot

#Genomewise plot
if(plot.type == "Genomewise")
{
#print("Manhattan ploting Genomewise")
#Set corlos for chromosomes
nchr=max(chm.to.analyze)
#nchr=length(chm.to.analyze)  #This cause problem ploting part of chromosome
ncycle=ceiling(nchr/band)
ncolor=band*ncycle
palette(rainbow(ncolor+1))
cycle1=seq(1,nchr,by= ncycle)
thecolor=cycle1

for(i in 2:ncycle){thecolor=c(thecolor,cycle1+(i-1))}
#print(thecolor)


#Sort by BP within CHR
GI.MP <- GI.MP[order(GI.MP[,2]),]
GI.MP <- GI.MP[order(GI.MP[,1]),]
color.vector <- rep(c("orangered","navyblue"),numCHR)
ticks=NULL
lastbase=0

#change base position to accumulatives (ticks)
for (i in chm.to.analyze)
{
  index=(GI.MP[,1]==i)
  ticks <- c(ticks, lastbase+mean(GI.MP[index,2]))
  GI.MP[index,2]=GI.MP[index,2]+lastbase
  lastbase=max(GI.MP[index,2])
}

x0 <- as.numeric(GI.MP[,2])
y0 <- as.numeric(GI.MP[,3])
z0 <- as.numeric(GI.MP[,1])
position=order(y0,decreasing = TRUE)
index0=GAPIT.Pruning(y0[position],DPP=DPP)
index=position[index0]
x=x0[index]
y=y0[index]
z=z0[index]

#Extract QTN
QTN=GI.MP[which(GI.MP[,borrowSlot]==1),]

#Draw circles with same size and different thikness
size=1
ratio=5
base=1
themax=max(y)
themin=min(y)
wd=((y-themin+base)/(themax-themin+base))*size*ratio
s=size-wd/ratio/2
y.lim <- ceiling(max(GI.MP[,3]))
#y.lim= 0.75
  pdf(paste("ZFst.", name.of.trait,".Genomewise.pdf" ,sep = ""), width = 15, height=3.5)
  par(mar = (c(3,4,2,2)+ 0.5), mgp=c(1.6,1,0))   ##  
  par(bty="l", lwd=1.5)  ## bty=l  the plot is coordinate instead of box
	mycols=rep(c("orangered","black","steelblue1","green4","navyblue"),max(z))## doulb dolor loop by chromosome, type = "h" is line; p is point,   
plot(y~x,ylab=expression(italic(paste("Z(F"[ST],")",sep = ""))),  ylim=c(0,y.lim), xaxs="i", yaxs="i" ,type = "p", lwd=1.50, pch=20, cex.axis=0.5, cex.lab=1.0 ,col=mycols[z], axes=FALSE,  lty=1, cex=0.35, cex.main=2.0, xlab="Chromosome")
 mtext(paste("",name.of.trait, sep=""), cex=1.5, font.main =1,  side=3, outer=TRUE,line=-1.5) 
#lines(y, x, type = "l")  
#Remove spacing around plotting area in r --- xaxs="i", yaxs="i"
#if(!is.null(dim(QTN)))abline(v=QTN[,2], lty = 2, lwd=1.5, col = "grey")
abline(h=5,col="dimgray",lty=2, lwd=1.0)  #MalVSInd

title(xlab="Chromosome")
 axis(1, at=ticks,tck=-0.01, cex.axis=1,labels=chm.to.analyze,tick=T, lwd=1.5, padj=-1)    ## lwd: line width tick=T, 
 #axis(2, at=0:y.lim,tck=-0.01, cex.axis=1,labels=0:y.lim,lwd=1.5, padj=1)     ## tck=-0.01 let the tck shor
 axis(2, tck=-0.01, cex.axis=1,lwd=1.5, padj=1)     ## tck=-0.01 let the tck shor
 box()
 dev.off()
print("Manhattan-Plot.Genomewise finished!")
#		mycols=rep(c("orangered","navyblue"),max(d$CHR))   col=thecolor[z], rep(c("orangered","navyblue"),z)
} #Genomewise plot


} #end of GAPIT.Manhattan

