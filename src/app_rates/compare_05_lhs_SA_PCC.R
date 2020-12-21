source("path_names_ar.R")
library(dplyr)
library(sensitivity)

# -----------------------------------------------------------
lhs_params <- read.csv(paste0(main_dir,'probabilistic_python/io/lhs_sampled_params.csv'),
                       sep=",", header=T)[,-1 ]

nsims = nrow(lhs_params)

sim_sums <- function(i,measurement){
  read.csv(paste0(main_dir,'probabilistic_python/input/swmm/input_',i,'/swmm_conv_to_vvwm_',measurement,'.csv'),
           sep=",", header=T)[,-1 ] %>% colSums()
}
# for Runoff
scr <- sim_sums(1,"runf"); for (i in 2:nsims){
  scr <- rbind(scr, sim_sums(i,"runf"))
}; row.names(scr) <- 1:nsims; scr <- as.data.frame(scr)
# for Bifenthrin
scb <- sim_sums(1,"bif"); for (i in 2:nsims){
  scb <- rbind(scb, sim_sums(i,"bif"))
}; row.names(scb) <- 1:nsims; scb <- as.data.frame(scb)

# -----------------------------------------------------------

runf.PCC <- bif.PCC <- data.frame()

for (i in c(1:113)){
  sub.i.pcc.r <- pcc(X = lhs_params, y = scr[,i])
  runf.PCC[i,names(lhs_params)] <- sub.i.pcc.r$PCC[,"original"]
  sub.i.pcc.b <- pcc(X = lhs_params, y = scb[,i])
  bif.PCC[i,names(lhs_params)] <- sub.i.pcc.b$PCC[,"original"]
}

# # so apparently subcatchment 65 is causing a problem.
# runf.PCC.cln <- runf.PCC; runf.PCC.cln[65,] <- NA
# bif.PCC.cln <- bif.PCC; bif.PCC.cln[65,] <- NA


rm(sub.i.pcc.b,sub.i.pcc.r,i)

save.image(paste0(main_dir,'src/app_rates/SA_results.RData'))
