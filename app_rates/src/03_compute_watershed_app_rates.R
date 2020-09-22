# ------------------------------------------------------------------------------
# compute watershed app rates for Pleasant Grove Creek watershed
# ------------------------------------------------------------------------------


# Using Luo,2015 methods

# To calulate urban pesticide use in the Pleasant Grove Creek Watershed (eastern portion):
#
#   [.1642 * PUR(Placer County)]
#
# where PUR(County) is the reported urban bifenthrin uses from the PUR database

mypath = "C:/Users/Julia Stelman/Desktop/Watershed/chelsvig_urban_pesticides/app_rates/calpip/" #JMS 9/22/20

# read in files
placer <- read.csv(file=paste0(mypath,"placer_09-17_with_homeowner.csv"),header=T, sep=",") #JMS 9/22/20

# create a null data frame to fill
# names its columns for what they will be filled with #JMS 9/22/20
final_df <- as.data.frame(matrix(data=NA, nrow=108, ncol=5)) #JMS 9/22/20
colnames(final_df) <- c("month", "year", "bif_kg_placer", "bif_kg_pgc", "bif_kgha_pgc")

# fill 
final_df$month <- placer$month
final_df$year <- placer$year
final_df$bif_kg_placer <- placer$bif_kg_with_home


# compute PGC watershed applications (kg)
final_df$bif_kg_pgc <- (.1642 * final_df$bif_kg_placer)


# compute PGC watershed application rate (kg/ha)
# 6485.67 ha
urban_ha <- 6485.67
final_df$bif_kgha_pgc <- final_df$bif_kg_pgc/urban_ha

# subset desired cols, write out
final_output <- final_df[, c("month", "year", "bif_kg_pgc", "bif_kgha_pgc")]
write.csv(final_output, file=paste0(mypath,"app_rates_09-17_pgc.csv"), row.names=F) #JMS 9/22/20



# ------------------------------------------------------------------------------
# the end
# ------------------------------------------------------------------------------