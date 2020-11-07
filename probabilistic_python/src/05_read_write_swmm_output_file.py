# ------------------------------------------------------------------------------------------
# read SWMM .rpt output file, and store desired outputs
# ------------------------------------------------------------------------------------------

# setup
import pandas as pd, os, numpy as np, dask
from datetime import date
import swmmtoolbox.swmmtoolbox as swmmtoolbox
from path_names import vvwm_path, dir_path
from prpy_bookkeeping import *

# nsims
nsims = 5

inp_dir_prefix = dir_path + r'\input\swmm\input_'

def save_and_continue(df,csv,msg = True):
    if not isinstance (msg,str):
        if msg == True:
            bn = os.path.basename(csv)
            dn = os.path.basename(os.path.dirname(csv))
            msg = "05: Saving intermediate version of data to <" + bn + "> in <" + dn + ">."
    if msg:
        logging.info(msg)
    df.to_csv(csv)
    return(df)

def save_and_finish(df,csv,msg = True):
    if not isinstance (msg,str):
        if msg == True:
            bn = os.path.basename(csv)
            dn = os.path.basename(os.path.dirname(csv))
            msg = "05: Saving final version of data to <" + bn + "> in <" + dn + ">."
    if msg:
        logging.info(msg)
    df.to_csv(csv)
    return("Finished " + dn)

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

# outfalls
outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42']

# list for the delayed tasks to be in
delayed_tasks = []

# the loop!
logging.info("05: Looping thru outfalls for navigating to each vwmm folder where its " + str(nsims) + " input folders will be created.")
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

#logging.info("05: Looping thru simulations to run swmmtoolbox on data and gather and munge output.")
# read in the .inp file subcatchment areas (to use later in script)
for rpt in range(1, nsims+1):
    sim_dir = inp_dir_prefix + str(rpt)

    # create blank list to hold subcatchment areas
    sub_list_area = []
    # read the .inp file
    sim_path = sim_dir + r'\NPlesantCreek.inp'
    ip_file = open(sim_path, "r")
    # skip x lines
    lines1 = ip_file.readlines()[55:]
    # close file
    ip_file.close() #JMS 10-15-20

    for thissub in range(0, 113):
        # grab the area
        listline = lines1[thissub].split()
        area = float(listline[3]) #JMS 10-15-20
        # insert into blank list
        sub_list_area.append(area)

    # binary output file
    sim_bin_path = sim_dir + r'\NPlesantCreek.out'

    # extract swmm outputs with swmmtoolbox
    lab1 = 'subcatchment,,Runoff_rate'
    lab2 = 'subcatchment,,Bifenthrin'
    runf_stack = dask.delayed(swmmtoolbox.extract)(sim_bin_path, lab1)
    bif_stack = dask.delayed(swmmtoolbox.extract)(sim_bin_path, lab2)

    # resample to daily average and save as new dataframe
    runf_davg = runf_stack.resample('D').mean()
    bif_davg = bif_stack.resample('D').mean()

    # write out swmm daily average outputs
    runf_to_conv = dask.delayed(save_and_continue)(runf_davg, sim_dir + r'\swmm_output_davg_runf.csv')
    bif_to_conv = dask.delayed(save_and_continue)(bif_davg, sim_dir + r'\swmm_output_davg_bif.csv')

    # Conversion for runf and bif
    runf_to_conv = runf_to_conv.mul(86400).mul(0.01).div(sub_list_area)
    bif_to_conv = bif_to_conv.mul(runf_to_conv.values)

    # Write out converted swmm outputs for runoff and bifenthrin
    runf_to_conv = dask.delayed(save_and_continue)(runf_to_conv, sim_dir + r'\swmm_conv_to_vvwm_runf.csv')
    bif_to_conv = dask.delayed(save_and_continue)(bif_to_conv, sim_dir + r'\swmm_conv_to_vvwm_bif.csv')

    for o in outfalls:
        outfall_dir = vvwm_path + o
        # subset subcatchment outputs for each vvwm
        outfall_path = outfall_dir + o + r'.csv'
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
        runf_out = outfall_dir + r'\input_' + str(rpt) + r'\runf_for_vvwm' + sfx_o
        bif_out = outfall_dir + r'\input_' + str(rpt) + r'\bif_for_vvwm' + sfx_o
        
        runf_msg = dask.delayed(save_and_finish)(runf_sub, runf_out)
        bif_msg = dask.delayed(save_and_finish)(bif_sub, bif_out)
        delayed_tasks.extend([runf_msg, bif_msg])

dask.delayed(print)(delayed_tasks).compute()
