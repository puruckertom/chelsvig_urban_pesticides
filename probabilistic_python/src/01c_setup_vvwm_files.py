# ------------------------------------------------------------------------------------------
# create .zts file for vvwm deterministic simulation
# ------------------------------------------------------------------------------------------

# setup
import pandas as pd, os, glob

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
    determ_input = outfall_path + r'\determ'

    # grab bif and runf .csv files

    # # text_files = glob.glob(determ_input + "\*.csv", recursive=True)
    # # bif_df = pd.read_csv(text_files[0])
    # # runf_df = pd.read_csv(text_files[2]) # changed to 2 after running 01d, since that adds another .csv file

    bif_df = pd.read_csv(glob.glob(determ_input + "\bif_for_vvwm_*.csv", recursive=True)[0]) #JMS 10-15-20
    runf_df = pd.read_csv(glob.glob(determ_input + "\runf_for_vvwm_*.csv", recursive=True)[0]) #JMS 10-15-20

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
    vvwm_df.to_csv(determ_input + r'\output.zts', header=False, index=False, sep=',')

    # define locations
    file_name = determ_input + r'\output.zts'
    dummy_file = determ_input + r'\temp.zts'

    # open original zts in read, dummy in write
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # write blanks to dummy file
        write_obj.write('\n\n\n') #JMS 10-15-20
        # read lines from original and append to dummy file
        for line in read_obj:
            write_obj.write(line)

    # remove original file
    os.remove(file_name)
    # rename dummy file as original file
    os.rename(dummy_file, file_name)
