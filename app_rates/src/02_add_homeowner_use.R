# ------------------------------------------------------------------------------
# add in homeowner usage
# ------------------------------------------------------------------------------

mypath = "C:/Users/Julia Stelman/Desktop/Watershed/chelsvig_urban_pesticides/app_rates/calpip/" #JMS 9/22/20

# read in files
placer <- read.csv(file=paste0(mypath,"placer_09-17.csv"), header=T) #JMS 9/22/20

# make new df
placer_2 <- placer


# compute homeowner rates (estimated as 25% of professional use (TDC, 2010) (CALFED, 2011))
placer_2$bif_kg_with_home <- placer$bif_kg + (placer$bif_kg*.25)


# write out files
write.csv(placer_2, file=paste0(mypath,"placer_09-17_with_homeowner.csv"), row.names=F)


# ------------------------------------------------------------------------------
# the end
# ------------------------------------------------------------------------------