# ------------------------------------------------------------------
# Latin Hypercube sampling of parameters for VVWM
# ------------------------------------------------------------------

# setup environment
import os, pandas as pd
from pyDOE import *
from scipy.stats import uniform
from path_names import dir_path

# number of simulations
nsims = 5

# import parameter ranges table
param_ranges = pd.read_csv(dir_path + r'\input\lhs\lhs_param_ranges_vvwm.csv')
print(param_ranges)

# create list of input parameter names
param_names = param_ranges["Parameter"].to_list()

# conduct lhs sampling
lhs_design = lhs(n=len(param_names), samples=nsims)
print("LHS Design w/o Uniform: ","\n",lhs_design.round(2))

for i in range(0,len(param_names)):
    lhs_design[:,i] = param_ranges.loc[i,"Min"] + (lhs_design[:,i])*(param_ranges.loc[i,"Range"]) #JMS 10-20-20
print("Uniformly Sampled from LHS Design: ", "\n", lhs_design)

# convert to data frame
lhs_df = pd.DataFrame(lhs_design, columns=param_names)
print(round(lhs_df,3))

# write out
lhs_df.to_csv(dir_path + r'\io\lhs_sampled_params_vvwm.csv')
