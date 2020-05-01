# -------------------------------------------------------------------------
# obtain swmm output time series data
# -------------------------------------------------------------------------

# set up
library(swmmr)
nsims = 5


# loop through all sims
# for (i in 1:nsims){

}

# select .inp file
simfolder <- paste('C:/Users/echelsvi/git/chelsvig_urban_pesticides/probabilistic_python/input/swmm/input_', i,sep="")
simfile <- paste(simfolder, "/NPlesantCreek",".out", sep="")
file.exists(simfile)

# to see what's available in output file
content <- get_out_content(file=simfile)


# read swmm results -- total runoff for watershed
results_runf <- data.frame(read_out(simfile, iType = 3, vIndex = 4)) 

# make edits to results
# move index column to first column [duplicate]
results_runf <- cbind(Date = rownames(results_runf), results_runf)
rownames(results_runf) <- 1:nrow(results_runf)
date <- results_runf$Date

# save results
# write.csv(results_runf, file = paste(swmmdir, "io/results_runf.csv", sep = ""))




# read swmm results -- pesticide washoff for a single subcatchment
bif_washf <- matrix(, ncol=113, nrow=dim(results_runf)[1])
bif_washf <- as.data.frame(bif_washf)

for (j in 1:113){
  subcatch <- paste("S", as.character(j), sep="")
  results_bif<- data.frame(read_out(simfile, iType = 0, object_name = subcatch , vIndex = 8))
  
  bif_washf[,j] <- results_bif$washoff_concentration_of_pollutant_Bifenthrin
  names(bif_washf)[names(bif_washf)== paste("V",j,sep="")] <- subcatch
}
bif_washf$date <- date
bif_washf$total_bif_washf <- apply(results_bif, MARGIN = 1, FUN=sum)





# ---------------------------------------------------------------
# the end
# ---------------------------------------------------------------