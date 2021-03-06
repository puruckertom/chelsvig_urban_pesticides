# ------------------------------------------------------------------------------------------
# read SWMM .rpt output file, and store desired outputs
# ------------------------------------------------------------------------------------------

# setup
import pandas as pd, os, numpy as np, dask
from datetime import date
# import swmmtoolbox.swmmtoolbox as swmmtoolbox
from path_names import vvwm_path, dir_path
from prpy_bookkeeping import *
loginfo = log_prefixer("05")

# number of simulations
try:
    nsims = main.nsims
except AttributeError:
    nsims = 5

inp_dir_prefix = os.path.join(dir_path, "input", "swmm", "input_")

# save the date columns for the csvs we will be making at the very end. 
datedf = pd.DataFrame({"date": pd.date_range(start='1/1/2009', periods=3287, freq='D')})
datedf['year'] = datedf['date'].dt.year
datedf['month'] = datedf['date'].dt.month
datedf['day'] = datedf['date'].dt.day
dates = datedf.date.tolist()
years = datedf.year.tolist()
months = datedf.month.tolist()
days = datedf.day.tolist()

runf_df_cols, runf_df_rows, bif_df_cols, bif_df_rows = 113, 3287, 113, 3287

outfalls = ['outfall_31_26', 'outfall_31_28', 'outfall_31_29', 'outfall_31_35',
            'outfall_31_36', 'outfall_31_38', 'outfall_31_42']

# list for the delayed tasks to be in
delayed_tasks = []

# the loop!
loginfo("Looping thru outfalls for navigating to each vwmm folder where its " + str(nsims) + " input folders will be created.")
for o in outfalls:
    # set pathways
    outfall_dir = os.path.join(vvwm_path, o)

    # create vvwm prob. sim. input folders
    for Ite in range(1, nsims + 1):
        new_dir = os.path.join(outfall_dir, "input_" + str(Ite))

        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
            print("Folder ", Ite, " created")
        else:
            print("Folder ", Ite, "already exists")

#loginfo("Looping thru simulations to run swmmtoolbox on data and gather and munge output.")
# read in the .inp file subcatchment areas (to use later in script)
for rpt in range(1, nsims+1):
    sim_dir = inp_dir_prefix + str(rpt)

    # create blank list to hold subcatchment areas
    sub_list_area = []
    # read the .inp file
    sim_path = os.path.join(sim_dir, "NPlesantCreek.inp")
    ip_file = open(sim_path, "r")
    # skip x lines
    lines1 = ip_file.readlines()[55:]
    # close file
    ip_file.close() #JMS 10-15-20

    for thissub in range(113):
        # grab the area
        listline = lines1[thissub].split()
        area = float(listline[3]) #JMS 10-15-20
        # insert into blank list
        sub_list_area.append(area)

    # write out swmm daily average outputs
    runf_to_conv = dask.delayed(pd.read_csv)(os.path.join(sim_dir, "swmm_output_davg_runf.csv"), index_col = 0)
    bif_to_conv = dask.delayed(pd.read_csv)(os.path.join(sim_dir, "swmm_output_davg_bif.csv"), index_col = 0)

    # Conversion for runf and bif
    runf_to_conv = runf_to_conv.mul(86400).mul(0.01).div(sub_list_area)
    bif_to_conv = bif_to_conv.mul(runf_to_conv.values)

    # Write out converted swmm outputs for runoff and bifenthrin
    runf_to_conv = dask.delayed(save_and_continue)(runf_to_conv, os.path.join(sim_dir, "swmm_conv_to_vvwm_runf.csv"))
    bif_to_conv = dask.delayed(save_and_continue)(bif_to_conv, os.path.join(sim_dir, "swmm_conv_to_vvwm_bif.csv"))

    for o in outfalls:
        outfall_dir = os.path.join(vvwm_path, o)
        # subset subcatchment outputs for each vvwm
        outfall_path = os.path.join(outfall_dir, o + ".csv")
        # declare which columns need to be subset
        sub_ids = (pd.read_csv(outfall_path, header = 0, usecols=['Subcatchment_ID']) - 1).sum(1).tolist()
        
        # Now, to subset:
        # make list where the elements at included indices are 1s and the other elements are 0s
        slicer = [(1 if x in sub_ids else np.nan) for x in range(113)]
        # now multiply it by the df
        runf_sub = (runf_to_conv * slicer).dropna(1)
        bif_sub = (bif_to_conv * slicer).dropna(1)

        # add a total sum column and date columns
        runf_sub=runf_sub.assign(runf_sum = runf_sub.sum(axis=1), date = dates, year = years, month = months, day = days)
        bif_sub=bif_sub.assign(bif_sum = bif_sub.sum(axis=1), date = dates, year = years, month = months, day = days)

        # write out dataframes
        sfx_o = outfall_path[-9:]
        runf_out = os.path.join(outfall_dir, "input_" + str(rpt), "runf_for_vvwm" + sfx_o)
        bif_out = os.path.join(outfall_dir, "input_" + str(rpt), "bif_for_vvwm" + sfx_o)
        
        runf_msg = dask.delayed(save_and_finish)(runf_sub, runf_out)
        bif_msg = dask.delayed(save_and_finish)(bif_sub, bif_out)
        delayed_tasks.extend([runf_msg, bif_msg])

dask.delayed(print)(delayed_tasks).compute()
