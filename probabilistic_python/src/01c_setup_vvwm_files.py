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

outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42',]

# loop through each outfall to create its vvwm.zts input file
for o in outfalls:
    # set pathways
    outfall_path = vvwm_path + o
    determ_input = outfall_path + r'\inputs\determ'
    filelist = os.listdir(determ_input)
    bif_df = pandas.read_csv(determ_input + r'\\' + filelist[0])
    runf_df = pandas.read_csv(determ_input + r'\\' + filelist[1])

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
    vvwm_df = pandas.concat([runf_sub, bif_sub], axis=1)

    # read out into comma-deliminated .txt file
    vvwm_df.to_csv(determ_input + r'\vvwm_input.zts', header=None, index=None, sep=',')

