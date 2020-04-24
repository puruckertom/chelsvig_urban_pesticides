# ------------------------------------------------------------------------------
# add in homeowner usage
# ------------------------------------------------------------------------------

# read in files
placer <- read.csv(file="C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/calpip/placer_09-17.csv", header=T)

# make new df
placer_2 <- placer


# compute homeowner rates (estimated as 25% of professional use (TDC, 2010) (CALFED, 2011))
placer_2$bif_kg_with_home <- placer$bif_kg + (placer$bif_kg*.25)


# write out files
write.csv(placer_2, file="C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/calpip/placer_09-17_with_homeowner.csv", row.names=F)


# ------------------------------------------------------------------------------
# the end
# ------------------------------------------------------------------------------