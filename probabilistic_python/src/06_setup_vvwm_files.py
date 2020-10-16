# ------------------------------------------------------------------------------------------
# create .zts file for vvwm probabilistic simulation
# ------------------------------------------------------------------------------------------

# setup
import pandas as pd, os, glob
from path_names import vvwm_path

# specify location
# print(os.path.abspath(os.curdir))
# os.chdir("..")
# dir_path = os.path.abspath(os.curdir)
# print(dir_path)

# vvwm_path = dir_path + r'\input\vvwm'
# print(vvwm_path)

outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42',]

nsims = 5

# loop through each outfall to create its vvwm.zts input file
for o in outfalls:

    # set pathways
    outfall_dir = vvwm_path + o
    for Ite in range(1, nsims + 1):
        input_dir = outfall_dir + r'\input_' + str(Ite)

        # grab bif and runf .csv files
        # text_files = glob.glob(input_dir + "\*.csv", recursive=True)
        # bif_df = pd.read_csv(text_files[0])
        # runf_df = pd.read_csv(text_files[2]) # todo will need to change to '2' after run vvwm which will create another .csv

        bif_df = pd.read_csv(glob.glob(input_dir + "\bif_*.csv", recursive=True)[0])
        runf_df = pd.read_csv(glob.glob(input_dir + "\runf_*.csv", recursive=True)[0])

        # vvwm .zts file format:
        # year,month,day,runf(cm/ha/day),0,bif(g/ha/day),0

        # cols of zero
        runf_df.loc[:, 'B'] = 0
        bif_df.loc[:, "MEp"] = 0

        runf_df.head()

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
            for line in read_file:
                write_file.write(line)

        # remove original file
        os.remove(swmm_out_path)
        # rename dummy file as original file
        os.rename(temp_path, swmm_out_path)
