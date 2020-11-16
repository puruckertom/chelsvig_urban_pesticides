# ------------------------------------------------------------------
# Latin Hypercube sampling of parameters for SWMM
# ------------------------------------------------------------------

# setup environment
import os, pandas as pd
from pyDOE import *
from scipy.stats import uniform
from path_names import dir_path
from prpy_bookkeeping import *

# number of simulations
nsims = 5

# import parameter ranges table
loginfo("Reading in lhs parameter range data from <" + dir_path + "\input\lhs\lhs_param_ranges.csv>.")
param_ranges = pd.read_csv(dir_path + r'\input\lhs\lhs_param_ranges.csv')
print(param_ranges)

# create list of input parameter names
param_names = param_ranges["Parameter"].to_list()

# parameter conditions:
# por >= fc, fc >= wp,

# conduct lhs sampling
lhs_design = lhs(n=len(param_names), samples=3*nsims)
lhs_design = lhs_design[np.where(lhs_design[:,11]<lhs_design[:,10])[0][:5]] #JMS 10-20-20
print("LHS Design w Uniform: ","\n",lhs_design.round(2)) #JMS 10-20-20

# uniformly sample
for i in range(0,len(param_names)):#-1): -JMS 10-20-20
    lhs_design[:,i] = param_ranges.loc[i,"Min"] + (lhs_design[:,i])*(param_ranges.loc[i,"Range"]) #JMS 10-20-20

# convert to data frame
lhs_df = pd.DataFrame(lhs_design, columns=param_names)
print(round(lhs_df,3))

# write out
logging.info("02: Writing generated lhs parameter value data into <" + dir_path + "\io\lhs_sampled_params.csv>.")
lhs_df.to_csv(dir_path + r'\io\lhs_sampled_params.csv')


