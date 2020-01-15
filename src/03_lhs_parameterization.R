
# ------------------------------------------------------------------
# Latin Hypercube sampling of parameters
# ------------------------------------------------------------------

# number of simulations 
Nsims <- 2

#simulation start and end (mm/dd/yyyy format)
simstart <- "01/01/2013"
simend <- "1/1/2014"


# list input paramters
input_parameters <- c("NImperv","NPerv")

# import parameter ranges table
param_ranges <- read.csv(paste(swmmdir,"input/lhs_param_ranges.csv",sep=""),
                         header=TRUE, sep= ",", stringsAsFactors=FALSE, row.names=NULL)



# ------------------------------------------------------------------
# LHS
# ------------------------------------------------------------------

# conduct Latin Hypercube Sampling for each input parameter
quantile_list <- randomLHS(Nsims, length(input_parameters)) 
dimnames(quantile_list ) <- list(NULL, input_parameters) 

# input_list  is now a uniformly distributed Latin hypercube 
head(quantile_list )

# set up a df to store the randomly sampled parameter values
input_list <- data.frame(matrix(NA,nrow=dim(quantile_list)[1],ncol=dim(quantile_list)[2]))

# for each parameter, sample from uniform distr. w/in parameter's range
for(i in 1:ncol(quantile_list)){
  #create quasi random numbers
  draw <- round(qunif(quantile_list[,i], min = param_ranges[i,2], max = param_ranges[i,3]),3)
  input_list[,i] <- draw
}

# input_list is now a uniformly distr. Latin Hypercube
input_list
colnames(input_list) <- c(input_parameters) 


# show the parameters are sampled from a uniform distribution - histogram, plot examples
hist(input_list$Nimperv,main="Histogram", xlab="Impervious", border="darkblue", col="gray")
plot(input_list$NPerv, pch = 19, col = "orange")

# write out the file
write.csv(input_list, file = paste(swmmdir, "io/inputlist_swmm.csv", sep = ""))



# --------------------------------------------------------------------
# the end
# --------------------------------------------------------------------