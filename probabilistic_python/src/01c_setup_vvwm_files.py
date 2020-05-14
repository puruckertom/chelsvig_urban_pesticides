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

vvwm_path = dir_path + r'\input\vvwm'
print(vvwm_path)
determ_inputs = vvwm_path + r'\inputs\determ'
print(determ_inputs)
determ_outputs = vvwm_path + r'\outputs\determ'
print(determ_outputs)

# todo read in all the files that contain a string
# read in all the .csv files
runf_df = pandas.read_csv(determ_inputs + r'\subcatchment_runf.csv')
bif_df = pandas.read_csv(determ_inputs + r'\subcatchment_bif.csv')

# vvwm .zts file format:
# year,month,day,runf(cm/ha/day),0,bif(g/ha/day),0

# todo convert runf and bif units

# cols of zero
runf_df.loc[:, 'B'] = 0
bif_df.loc[:, "MEp"] = 0

# subset the desired cols from df's and join together
runf_sub = runf_df[["year", "month", "day", "runf_sum", "B"]]
bif_sub = bif_df[["bif_sum", "MEp"]]

# combine
vvwm_df = pandas.concat([runf_sub,bif_sub], axis=1)

# read out into comma-deliminated .txt file
vvwm_df.to_csv(determ_outputs + r'\vvwm_input.zts', header=None, index=None, sep=',')
