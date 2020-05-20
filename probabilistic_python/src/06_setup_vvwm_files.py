# ------------------------------------------------------------------------------------------
# create .zts file for vvwm probabilistic simulation
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

    for Ite in range(1, nsims + 1):
        folder = r'\input_' + str(Ite)
        input_folder = outfall_path + folder
        filelist = os.listdir(input_folder)
        bif_df = pandas.read_csv(input_folder + r'\\' + filelist[0])
        runf_df = pandas.read_csv(input_folder + r'\\' + filelist[1])

        # vvwm .zts file format:
        # year,month,day,runf(cm/ha/day),0,bif(g/ha/day),0

        # cols of zero
        runf_df.loc[:, 'B'] = 0
        bif_df.loc[:, "MEp"] = 0

        # subset the desired cols from df's and join together
        runf_sub = runf_df[["year", "month", "day", "runf_sum", "B"]]
        bif_sub = bif_df[["bif_sum", "MEp"]]

        # combine
        vvwm_df = pandas.concat([runf_sub, bif_sub], axis=1)

        # read out into comma-delimited .txt file
        vvwm_df.to_csv(input_folder + r'\output.zts', header=False, index=False, sep=',')

