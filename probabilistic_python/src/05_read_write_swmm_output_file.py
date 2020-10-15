# ------------------------------------------------------------------------------------------
# read SWMM .rpt output file, and store desired outputs
# ------------------------------------------------------------------------------------------

# setup
import pandas as pd, os, numpy as np
from datetime import date
import swmmtoolbox.swmmtoolbox as swmmtoolbox

# nsims
nsims = 5

# specify location
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

input_path = dir_path + r'\input\swmm\input_'
output_path = dir_path + r'\input\vvwm\input_'
swmm_path = dir_path + r'\input\swmm'
vvwm_path = dir_path + r'\input\vvwm'

# outfalls
outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42',]

# the loop!
for o in outfalls:
    # set pathways
    outfall_path = vvwm_path + o

    # create vvwm prob. sim. input folders
    for Ite in range(1, nsims + 1):
        newfol = r'\input_' + str(Ite)
        newdir = outfall_path + newfol

    if not os.path.exists(newdir):
        os.mkdir(newdir)
        print("Folder ", Ite, " created")
    else:
        print("Folder ", Ite, "already exists")
    os.getcwd()
    os.chdir(newdir)

    # read in the .inp file subcatchment areas (to use later in script)
    for rpt in range(1, nsims+1):
        folder_path = input_path + str(rpt)

        # read the .inp file
        inp_file = folder_path + r'\NPlesantCreek.inp'
        ipfile = open(inp_file, "r")

        # create blank list to hold subcatchment areas
        sub_list_area = []

        # skip x lines
        lines1 = ipfile.readlines()[55:]

        # close file
        ipfile.close() #JMS 10-15-20

        for thissub in range(0, 113):
            # grab the area
            thisline = lines1[thissub]
            listline = thisline.split()
            area = float(listline[3]) #JMS 10-15-20

            # insert into blank list
            sub_list_area.append(area)

        # binary output file
        bin_file = folder_path + r'\NPlesantCreek.out'

        # extract swmm outputs with swmmtoolbox
        lab1 = 'subcatchment,,Runoff_rate'
        lab2 = 'subcatchment,,Bifenthrin'
        extract_runf = swmmtoolbox.extract(bin_file, lab1)
        extract_bif = swmmtoolbox.extract(bin_file, lab2)

        # write out swmm outputs
        extract_runf.to_csv(folder_path + r'\swmm_output_runf.csv')
        extract_bif.to_csv(folder_path + r'\swmm_output_bif.csv')

        # read file back in, delete first col
        swmmout_runf = pd.read_csv(folder_path + r'\swmm_output_runf.csv')
        del swmmout_runf['Unnamed: 0']
        swmmout_bif = pd.read_csv(folder_path + r'\swmm_output_bif.csv')
        del swmmout_bif['Unnamed: 0']

        # create pandas datetime col
        df = pd.DataFrame(
            {'datetime': pd.date_range('2009-01-01 01:00:00', '2018-01-01', freq='1H', closed='left')} #JMS 10-15-20
        )

        # combine to swmm output with datetime
        runf_stack = pd.concat([swmmout_runf, df], axis=1)
        bif_stack = pd.concat([swmmout_bif, df], axis=1)

        # set datetime as DatetimeIndex
        runf_stack = runf_stack.set_index('datetime')
        bif_stack = bif_stack.set_index('datetime')

        # resample to daily average and save as new dataframe
        runf_davg = runf_stack.resample('D').mean()
        bif_davg = bif_stack.resample('D').mean()

        # write out swmm daily outputs
        runf_davg.to_csv(folder_path + r'\swmm_output_davg_runf.csv')
        bif_davg.to_csv(folder_path + r'\swmm_output_davg_bif.csv')

        # copy
        runf_to_conv = runf_davg.copy()
        bif_to_conv = bif_davg.copy()

        # specify loop variables
        runf_df_cols = len(runf_to_conv.columns)  # 113
        runf_df_rows = len(runf_to_conv)  # 3287
        bif_df_cols = len(bif_to_conv.columns)
        bif_df_rows = len(bif_to_conv)

        # conversion for runf
        for c in range(0, runf_df_cols):
            col_name = "subcatchment_S" + str(c + 1) + "_Runoff_rate"

            # define subcatchment's area
            this_area = sub_list_area[c]

            # perform conversion
            runf_to_conv[col_name] = (runf_to_conv[col_name] * 86400 * 0.01) / this_area

        # write out converted swmm outputs
        runf_to_conv.to_csv(folder_path + r'\swmm_conv_to_vvwm_runf.csv')

        # conversion for bifenthrin conc.
        for c in range(0, bif_df_cols):

            # define subcatchment's area
            this_area = sub_list_area[c]

            for r in range(0, bif_df_rows):
                # define the runoff value (m3/day)
                this_runf = runf_davg.iloc[r, c] * 864000

                # compute g/ha/day
                bif_to_conv.iloc[r, c] = ((bif_to_conv.iloc[r, c]) * 1000 * this_runf) / (1.0e6 * this_area)

        # write out converted swmm outputs
        bif_to_conv.to_csv(folder_path + r'\swmm_conv_to_vvwm_bif.csv')

        # subset subcatchment outputs for each vvwm
        outfall_file = outfall_path + '\\' + o + r'.csv'

        # declare which columns need to be subset
        sub_file = pd.read_csv(outfall_file)
        sublist = sub_file['Subcatchment_ID'].tolist()

        collist = [x - 1 for x in sublist]  # columns to subset from df

        # subset
        runf_sub = runf_to_conv.iloc[:, collist]
        bif_sub = bif_to_conv.iloc[:, collist]

        # add a total sum column
        runf_sub["runf_sum"] = runf_sub.sum(axis=1)
        bif_sub["bif_sum"] = bif_sub.sum(axis=1)

        # add a date column
        runf_sub['date'] = pd.date_range(start='1/1/2009', periods=len(runf_sub), freq='D')
        bif_sub['date'] = pd.date_range(start='1/1/2009', periods=len(bif_sub), freq='D')

        # separate date column too
        runf_sub['year'] = runf_sub['date'].dt.year
        runf_sub['month'] = runf_sub['date'].dt.month
        runf_sub['day'] = runf_sub['date'].dt.day

        bif_sub['year'] = bif_sub['date'].dt.year
        bif_sub['month'] = bif_sub['date'].dt.month
        bif_sub['day'] = bif_sub['date'].dt.day

        # write out dataframes
        substring = outfall_file[103: 112:]
        out_folder = outfall_path + r'\input_' + str(rpt)
        runf_out = out_folder + r'\runf_for_vvwm' + substring
        bif_out = out_folder + r'\bif_for_vvwm' + substring
        runf_sub.to_csv(runf_out)
        bif_sub.to_csv(bif_out)


