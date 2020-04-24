# ------------------------------------------------------------------
# Latin Hypercube sampling of parameters
# ------------------------------------------------------------------

# setup environment
import os, pandas, numpy
#import matplotlib.pyplot as plt
from smt.sampling_methods import LHS

# directory
swmmdir = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\probabilistic_python'

# number of simulations
nsims = 2

# simulation start and end (mm/dd/yyyy format)
simstart = "01/01/2009"
simend = "01/01/2018"

# import parameter ranges table
param_ranges = pandas.read_csv(os.path.join(swmmdir, r'input\lhs\lhs_param_ranges.csv'))
print(param_ranges.columns)
print(param_ranges.values)

# create list of input parameter names
input_parameters = param_ranges["Parameter"].to_list()
print(input_parameters)

# create empty list for min,max
row_list = []

# iterate over each param_ranges row
for index, rows in param_ranges.iterrows():
    # create list for the current row
    cur_list = [rows.Min, rows.Max]

    # append the list to the final list
    row_list.append(cur_list)

# print the list of param ranges
print(row_list)


# conduct lhs sampling
x_limits = numpy.array(row_list)
sampling = LHS(xlimits=x_limits)
lhs_list = sampling(nsims)
print(lhs_list)
print(type(lhs_list))



# # conduct Latin Hypercube Sampling for each input parameter
# quantile_list = randomLHS(Nsims, length(input_parameters))
# dimnames(quantile_list ) = list(NULL, input_parameters)
#
# # input_list  is now a uniformly distributed Latin hypercube
# head(quantile_list)
#
# # set up a df to store the randomly sampled parameter values
# input_list = data.frame(matrix(NA,nrow=dim(quantile_list)[1],ncol=dim(quantile_list)[2]))
#
# # for each parameter, sample from uniform distr. w/in parameter's range
# for(i in 1:ncol(quantile_list)):
#   #create quasi random numbers
#   draw = round(qunif(quantile_list[,i], min = param_ranges[i,2], max = param_ranges[i,3]),3)
#   input_list[,i] = draw
#
#
# # input_list is now a uniformly distr. Latin Hypercube
# input_list
# colnames(input_list) = c(input_parameters)
#
#
# # show the parameters are sampled from a uniform distribution - histogram, plot examples
# hist(input_list$Nimperv,main="Histogram", xlab="Impervious", border="darkblue", col="gray")
# plot(input_list$NPerv, pch = 19, col = "orange")
#
# # write out the file
# write.csv(input_list, file = paste(swmmdir, "io/inputlist_swmm.csv", sep = ""))



# --------------------------------------------------------------------
# the end
# --------------------------------------------------------------------