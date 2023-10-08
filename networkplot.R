print("In Network.R")
install.packages("networktools")
install.packages("smacof")
install.packages("MPsychoR")
install.packages("psych")
install.packages("eigenmodel")
install.packages("dplyr")
install.packages("NetworkComparisonTest")
require("networktools")
library("MPsychoR")
library("smacof")
library("qgraph")
library("psych")
library("eigenmodel")
library("dplyr")
library("ggplot2")
library("qgraph")
library("networktools")
library("IsingSampler")
library("IsingFit")
library("bootnet")


f'dt <- read.csv("{uploaded_file.name}", header=TRUE)'
f'netdt1 <- select(dt, {columns_to_select_str})'
net1 <- qgraph(cor_auto(netdt1), n = nrow(netdt1), lambda.min.ratio = 0.05, default = "EBICglasso", layout="spring", vsize = 16, gamma = 0.2, tuning = 0.2, refit = TRUE)



png("qgraph_plot.png")
qgraph(net1, maximum=0.29)
dev.off()
