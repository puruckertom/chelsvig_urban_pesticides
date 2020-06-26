# ------------------------------------------------------------------
# Latin Hypercube sampling of parameters for SWMM
# ------------------------------------------------------------------

# setup environment
import os, pandas
from pyDOE import *
from scipy.stats import uniform

# specify location
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

# number of simulations
nsims = 5

# import parameter ranges table
param_ranges = pandas.read_csv(dir_path + r'\input\lhs\lhs_param_ranges.csv')
print(param_ranges)

# create list of input parameter names
param_names = param_ranges["Parameter"].to_list()

# parameter conditions:
# por >= fc, fc >= wp,

# conduct lhs sampling
lhs_design = lhs(n=len(param_names), samples=nsims)
print("LHS Design w/o Uniform: ","\n",lhs_design)

# uniformly sample
for i in range(0,len(param_names)-1):
    lhs_design[:,i] = uniform.rvs(loc=param_ranges.loc[i,"Min"], scale=param_ranges.loc[i,"Range"], size=nsims)
print("Uniformly Sampled from LHS Design: ", "\n", lhs_design)

# convert to data frame
lhs_df = pandas.DataFrame(lhs_design, columns=param_names)
print(lhs_df)

# redo parameters that must meet conditions
# 0.024 <= wp < fc or 0.265
vec_fc = lhs_df["FC"]
vec_wp = lhs_df["WP"]

wp_min = 0.024
for i in range(0, len(vec_fc)):
    fc_value = vec_fc[i]
    wp_value = vec_wp[i]
    print("FC =", fc_value, "and WP =", wp_value)

    if wp_value > fc_value:
        new_lhs = lhs(n=1, samples=1)
        new_lhs = uniform.rvs(loc=wp_min, scale=(fc_value - wp_min), size=1)
        vec_wp[i] = new_lhs

print(vec_wp)

lhs_df["WP"] = vec_wp
print(lhs_df)

# write out
lhs_df.to_csv(dir_path + r'\io\lhs_sampled_params.csv')


