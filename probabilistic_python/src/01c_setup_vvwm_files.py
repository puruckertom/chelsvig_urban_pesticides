# ------------------------------------------------------------------------------------------
# create .zts file for vvwm (for probabilistic sims)
# ------------------------------------------------------------------------------------------

# setup
import pandas, os

# specify location
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

input_path = dir_path + r'\input\swmm'
print(input_path)

# read in all the .csv files
runf_df = pandas.read_csv(input_path + r'\subcatchment_runf.csv')

bif_df = pandas.read_csv(input_path + r'\subcatchment_bif.csv')

# subset the desired cols from df's and join together
#todo will need to add the other .zts variables
runf_sub = runf_df[["year", "month", "day", "runf_sum"]]
bif_sub = bif_df[["bif_sum"]]

#todo will need to add the other .zts variables
vvwm_df = pandas.concat([runf_sub,bif_sub], axis=1)

# read out into comma-deliminated .txt file
vvwm_df.to_csv(input_path + r'\vvwm_input.zts', header=None, index=None, sep=',')
