# ------------------------------------------------------------------------------
# add in homeowner usage
# ------------------------------------------------------------------------------

source("path_names_ar.R")

# read in files
placer <- read.csv(file=paste0(calpip_dir,"placer_09-17.csv"), header=T) #JMS 9/22/20

# make new df
placer_2 <- placer


# compute homeowner rates (estimated as 25% of professional use (TDC, 2010) (CALFED, 2011))
placer_2$bif_kg_with_home <- placer$bif_kg + (placer$bif_kg*.25)


# write out files
write.csv(placer_2, file=paste0(calpip_dir,"placer_09-17_with_homeowner.csv"), row.names=F)


# ------------------------------------------------------------------------------
# the end
# ------------------------------------------------------------------------------