## usage: Rscript ~/script/Treemix/plot/plotting.R bootstrap_1 ../Pop.color
args<-commandArgs(T)
source("~/script/Treemix/plot/plotting_funcs.R")
plot_tree(args[1], args[2])
plot_resid(args[1], args[2])
