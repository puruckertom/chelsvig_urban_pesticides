source("path_names_ar.R")
library(dplyr)
library(sensitivity)

# -----------------------------------------------------------
lhs_params <- read.csv(paste0(main_dir,'probabilistic_python/io/lhs_sampled_params.csv'),
                       sep=",", header=T)[,-1 ]

sim_sums <- function(i,measurement){
  read.csv(paste0(main_dir,'probabilistic_python/input/swmm/input_',i,'/swmm_conv_to_vvwm_',measurement,'.csv'),
           sep=",", header=T)[,-1 ] %>% colSums()
}
# for Runoff
scr <- sim_sums(1,"runf"); for (i in 2:5){
  scr <- rbind(scr, sim_sums(i,"runf"))
}; row.names(scr) <- 1:5; scr <- as.data.frame(scr)
# for Bifenthrin
scb <- sim_sums(1,"bif"); for (i in 2:5){
  scb <- rbind(scb, sim_sums(i,"bif"))
}; row.names(scb) <- 1:5; scb <- as.data.frame(scb)

# -----------------------------------------------------------

# just use 3 params 4 now because we can't have more params than sims
rNI <- c(); rNP <- c(); rSI <- c(); bNI <- c(); bNP <- c(); bSI <- c()
for (i in 113){
  sub.i.pcc.r <- pcc(X = lhs_params[,1:3], y = scr[,i])
  rNI <- append(rNI,sub.i.pcc.r$PCC["NImperv","original"])
  rNP <- append(rNP,sub.i.pcc.r$PCC["NPerv","original"])
  rSI <- append(rSI,sub.i.pcc.r$PCC["SImperv","original"])
  sub.i.pcc.b <- pcc(X = lhs_params[,1:3], y = scb[,i])
  bNI <- append(rNI,sub.i.pcc.b$PCC["NImperv","original"])
  bNP <- append(rNP,sub.i.pcc.b$PCC["NPerv","original"])
  bSI <- append(rSI,sub.i.pcc.b$PCC["SImperv","original"])
}

par(mfrow = c(2,3))
sapply(list(rNI,rNP,rSI,bNI,bNP,bSI),hist)
