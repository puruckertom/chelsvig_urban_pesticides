# ------------------------------------------------------------------------------------------
# create .zts file for vvwm probabilistic simulation
# ------------------------------------------------------------------------------------------

# setup
import pandas as pd, os, glob
from path_names import vvwm_path
from bookkeeping import *

outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42']

nsims = 5

# loop through each outfall to create its vvwm.zts input file
logging.info("06: Looping thru outfalls for navigating to each vwmm folder where .zts files will be created in its " + nsims + " simulated input folders.")
for o in outfalls:

    # set pathways
    outfall_dir = vvwm_path + o
    logging.info("06: Looping thru simulations of " + o[1:] + " to create their .zts files by munging the data in their sets of .csv files.")
    for Ite in range(1, nsims + 1):
        input_dir = outfall_dir + r'\input_' + str(Ite)

        # grab bif and runf .csv files
        bif_df = pd.read_csv(glob.glob(input_dir + r'\bif_for*.csv', recursive=True)[0])
        runf_df = pd.read_csv(glob.glob(input_dir + r'\runf_for*.csv', recursive=True)[0])

        # vvwm .zts file format:
        # year,month,day,runf(cm/ha/day),0,bif(g/ha/day),0

        # cols of zero
        runf_df.loc[:, 'B'] = 0
        bif_df.loc[:, "MEp"] = 0

        print(runf_df.head(3))

        # subset the desired cols from df's and join together
        runf_sub = runf_df.loc[:, ["year", "month", "day", "runf_sum", "B"]]
        bif_sub = bif_df.loc[:, ["bif_sum", "MEp"]]

        # combine
        vvwm_df = pd.concat([runf_sub, bif_sub], axis=1)

        # read out into comma-delimited .txt file
        vvwm_df.to_csv(input_dir + r'\output.zts', header=False, index=False, sep=',')

        # define locations
        swmm_out_path = input_dir + r'\output.zts'
        temp_path = input_dir + r'\temp.zts'

        # open original zts in read, dummy in write
        with open(swmm_out_path, 'r') as read_file, open(temp_path, 'w') as write_file:
            # write blanks to dummy file
            write_file.write('\n\n\n')
            # read lines from original and append to dummy file
            write_file.writelines(read_file) #JMS 10-21-20

        # remove original file
        os.remove(swmm_out_path)
        # rename dummy file as original file
        os.rename(temp_path, swmm_out_path)
