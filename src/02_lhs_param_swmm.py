# ------------------------------------------------------------------
# Latin Hypercube sampling of parameters for SWMM
# ------------------------------------------------------------------

# setup environment
import os, pandas as pd, numpy as np
from pyDOE2 import lhs
from scipy.stats import uniform
from path_names import dir_path
from prpy_bookkeeping import *
loginfo = log_prefixer("02")

# number of simulations
try:
    nsims = main.nsims
except AttributeError:
    nsims = 5

# import parameter ranges table
loginfo("Reading in lhs parameter range data from <" + dir_path + r"\input\lhs\lhs_param_ranges.csv>.")
param_ranges = pd.read_csv(os.path.join(dir_path, "input", "lhs", "lhs_param_ranges.csv"))
print(param_ranges)

# create list of input parameter names
param_names = param_ranges["Parameter"].to_list()

# parameter conditions:
# por >= fc (happens automatically), fc >= wp, MaxRate>=MinRate

# conduct lhs sampling
lhs_design = lhs(n=len(param_names), samples=3*nsims)  # take 3x as many samples as needed, in case some don't meet conditions
# uniformly sample
for i in range(0,len(param_names)):
    lhs_design[:,i] = param_ranges.loc[i,"Min"] + (lhs_design[:,i])*(param_ranges.loc[i,"Range"])
# filter on conditions: fc >= wp, MaxRate >= MinRate
lhs_design = lhs_design.iloc[np.where(lhs_design.iloc[:,11]<lhs_design.iloc[:,10])[0]]  # fc >= wp
lhs_design = lhs_design.iloc[np.where(lhs_design.iloc[:,6]<lhs_design.iloc[:,5])[0]]  # MaxRate >= MinRate
lhs_design = lhs_design.head(nsims) # only take first nsims rows meeting conditions

# convert to data frame
lhs_df = pd.DataFrame(lhs_design, columns=param_names)
print(round(lhs_df,3))

# write out
loginfo("Writing generated lhs parameter value data into <" + dir_path + r"\io\lhs_sampled_params.csv>.")
lhs_df.to_csv(os.path.join(dir_path, "io", "lhs_sampled_params.csv"))


