# ------------------------------------------------------------------------------------------
# read SWMM .rpt output file, and store desired outputs
# ------------------------------------------------------------------------------------------

# setup
import pandas as pd, os, numpy as np
from datetime import date
import swmmtoolbox.swmmtoolbox as swmmtoolbox
from path_names import vvwm_path, dir_path

# nsims
nsims = 5

# specify location
# print(os.path.abspath(os.curdir))
# os.chdir("..")
# dir_path = os.path.abspath(os.curdir)
# print(dir_path)

inp_dir_prefix = dir_path + r'\input\swmm\input_'
# swmm_path = dir_path + r'\input\swmm'
# vvwm_path = dir_path + r'\input\vvwm'

# outfalls
outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42']

# the loop!
for o in outfalls:
    # set pathways
    outfall_dir = vvwm_path + o

    # create vvwm prob. sim. input folders
    for Ite in range(1, nsims + 1):
        new_dir = outfall_dir + r'\input_' + str(Ite)

    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
        print("Folder ", Ite, " created")
    else:
        print("Folder ", Ite, "already exists")
    # os.getcwd()
    # os.chdir(new_dir)

    # read in the .inp file subcatchment areas (to use later in script)
    for rpt in range(1, nsims+1):
        sim_dir = inp_dir_prefix + str(rpt)

        # read the .inp file
        sim_path = sim_dir + r'\NPlesantCreek.inp'
        ip_file = open(sim_path, "r")

        # create blank list to hold subcatchment areas
        sub_list_area = []

        # skip x lines
        lines1 = ip_file.readlines()[55:]

        # close file
        ip_file.close() #JMS 10-15-20

        for thissub in range(0, 113):
            # grab the area
            thisline = lines1[thissub]
            listline = thisline.split()
            area = float(listline[3]) #JMS 10-15-20

            # insert into blank list
            sub_list_area.append(area)

        # binary output file
        sim_bin_path = sim_dir + r'\NPlesantCreek.out'

        # extract swmm outputs with swmmtoolbox
        lab1 = 'subcatchment,,Runoff_rate'
        lab2 = 'subcatchment,,Bifenthrin'
        extract_runf = swmmtoolbox.extract(sim_bin_path, lab1)
        extract_bif = swmmtoolbox.extract(sim_bin_path, lab2)

        # write out swmm outputs
        extract_runf.to_csv(sim_dir + r'\swmm_output_runf.csv')
        extract_bif.to_csv(sim_dir + r'\swmm_output_bif.csv')

        # read file back in, delete first col
        swmmout_runf = pd.read_csv(sim_dir + r'\swmm_output_runf.csv')
        del swmmout_runf['Unnamed: 0']
        swmmout_bif = pd.read_csv(sim_dir + r'\swmm_output_bif.csv')
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
        runf_davg.to_csv(sim_dir + r'\swmm_output_davg_runf.csv')
        bif_davg.to_csv(sim_dir + r'\swmm_output_davg_bif.csv')

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
        runf_to_conv.to_csv(sim_dir + r'\swmm_conv_to_vvwm_runf.csv')

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
        bif_to_conv.to_csv(sim_dir + r'\swmm_conv_to_vvwm_bif.csv')

        # subset subcatchment outputs for each vvwm
        outfall_path = outfall_dir + '\\' + o + r'.csv'

        # declare which columns need to be subset
        sub_df = pd.read_csv(outfall_path)
        sublist = sub_df['Subcatchment_ID'].tolist()

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
        substring = outfall_path[103: 112:]
        runf_out = outfall_dir + r'\input_' + str(rpt) + r'\runf_for_vvwm' + substring
        bif_out = outfall_dir + r'\input_' + str(rpt) + r'\bif_for_vvwm' + substring
        runf_sub.to_csv(runf_out)
        bif_sub.to_csv(bif_out)


