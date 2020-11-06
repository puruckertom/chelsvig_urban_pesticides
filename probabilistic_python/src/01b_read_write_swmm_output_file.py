# ------------------------------------------------------------------------------------------
# read swmm .rpt output file, and store desired outputs
# ------------------------------------------------------------------------------------------

# setup
import os, pandas as pd, dask, numpy as np
import swmmtoolbox.swmmtoolbox as swmmtoolbox
from path_names import swmm_path, inp_path, bin_path, vvwm_path
from prpy_bookkeeping import *

outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42']

def save_and_continue(df,csv,msg = "01b: Saving intermediate version of data to <" + bn + "> in <" + dn + ">."):
    bn = os.path.basename(csv)
    dn = os.path.basename(os.path.dirname(csv))
    if msg:
        logging.info(msg)
    df.to_csv(csv)
    return(df)

def save_and_finish(df,csv,msg = "01b: Saving final version of data to <" + bn + "> in <" + dn + ">."):
    bn = os.path.basename(csv)
    dn = os.path.basename(os.path.dirname(csv))
    if msg:
        logging.info(msg)
    df.to_csv(csv)
    return("Finished " + dn)


# displays version number and system info
#swmmtoolbox.about()

# list the catalog of objects in output file
# list all available labels for the extract function
# swmmtoolbox.catalog(filename, itemtype='', header='default')
#swmmtoolbox.catalog(bin_path, itemtype='', header='default')

# list variables available for each type
# use this info for the 'var' portion of the 'extract' function parameter
# this shows the variable name and its index
# swmmtoolbox.listvariables(filename, header='default')
#swmmtoolbox.listvariables(bin_path, header='default')

# get the time series data for a particular object and variable
#swmmtoolbox.extract(filename, *labels)
# lables = 'type,name,var'
# labels require two commas and no spaces
# use 'catalog' and 'listvariables' for var parameters
# there is a wild card feature for labels, where leaving the part out
#   will return all labels that match all other parts.
lab1 = 'subcatchment,,Runoff_rate'
lab2 = 'subcatchment,,Bifenthrin'
#logging.info("01b: Getting the time series data for runoff rate and bifenthrin using swmmtoolbox's extract function.")
runf_stack = dask.delayed(swmmtoolbox.extract)(bin_path, lab1)
bif_stack = dask.delayed(swmmtoolbox.extract)(bin_path, lab2)

# resample to daily average and save as new dataframe
#logging.info("01b: Calculating the daily averages from the hourly timeseries of runoff rate and bifenthrin.")
runf_davg = runf_stack.resample('D').mean()
bif_davg = bif_stack.resample('D').mean()

# write out swmm daily outputs
#logging.info("01b: Writing daily average data to csv files.")
runf_to_conv = dask.delayed(save_and_continue)(runf_davg, swmm_path + r'\swmm_output_davg_runf.csv')
bif_to_conv = dask.delayed(save_and_continue)(bif_davg, swmm_path + r'\swmm_output_davg_bif.csv')

# # specify loop variables
runf_df_cols, runf_df_rows, bif_df_cols, bif_df_rows = 113, 3287, 113, 3287

# save the date columns for the csvs we will be making at the very end. 
datedf = pd.DataFrame({"date": pd.date_range(start='1/1/2009', periods=3287, freq='D')})
datedf['year'] = datedf['date'].dt.year
datedf['month'] = datedf['date'].dt.month
datedf['day'] = datedf['date'].dt.day
dates = datedf.date.tolist()
years = datedf.year.tolist()
months = datedf.month.tolist()
days = datedf.day.tolist()

# create blank list to hold subcatchment areas
sub_list_area = []
# read in the .inp file subcatchment areas
logging.info("01b: Opening the input file <" + inp_path + "> to read.")
ip_file = open(inp_path, 'r') #JMS 10-15-20
# skip x lines and read in the lines after
logging.info("01b: Reading lines from file")
lines1 = ip_file.readlines()[55:] #JMS 10-15-20
# close file 
logging.info("01b: Closing file.")
ip_file.close() #JMS 10-15-20

logging.info("01b: Looping thru lines in file and saving subcatchment area information into a list.")
for thissub in range(0, runf_df_cols):
    # grab the area
    thisline = lines1[thissub]
    listline = thisline.split()
    area = float(listline[3]) #JMS 10-15-20
    # insert into blank list
    sub_list_area.append(area)

# conversion for runf
#logging.info("01b: Replacing the runoff and bifenthrin values in the respective dataframes with their respective post-conversion values.")
runf_to_conv = runf_to_conv.mul(86400).mul(0.01).div(sub_list_area)
bif_to_conv = bif_to_conv.mul(runf_to_conv.values)
#logging.info("01b: Writing the tables with the converted runoff and bifenthrin values to csv files.")
runf_to_conv = dask.delayed(save_and_continue)(runf_to_conv, swmm_path + r'\swmm_conv_to_vvwm_runf.csv')
bif_to_conv = dask.delayed(save_and_continue)(bif_to_conv, swmm_path + r'\swmm_conv_to_vvwm_bif.csv')

delayed_tasks = []

# subset subcatchment outputs for each vvwm
logging.info("01b: Looping thru outfalls for subset the subcatchments for each vwmm folder.")
for o in outfalls:
    # set pathways
    outfall_dir = vvwm_path + o
    determ_dir = outfall_dir + r'\determ'
    outfall_path = outfall_dir + o + r'.csv'

    # declare which columns need to be subset for the respective outfall
    logging.info("01b: Reading in <" + r'\determ' + o + r'.csv' + "> to data frame.")
    sub_df = pd.read_csv(outfall_path)
    sublist = sub_df['Subcatchment_ID'].tolist()
    collist = [x - 1 for x in sublist]  # columns to subset from df

    # subset
    # make list where the elements at included indices are 1s and the other elements are 0s
    slicer = [(1 if x in collist else np.nan) for x in range(113)]
    # now multiply it by the df
    runf_sub = (runf_to_conv * slicer).dropna(1)
    bif_sub = (bif_to_conv * slicer).dropna(1)

    # add a total sum column and date columns
    runf_sub=runf_sub.assign(sums = runf_sub.sum(axis=1), date = dates, year = years, month = months, day = days)
    bif_sub=bif_sub.assign(sums = bif_sub.sum(axis=1), date = dates, year = years, month = months, day = days)

    # write out dataframes
    sfx_o = outfall_path[-9:] #JMS 10-19-20
    runf_out = determ_dir + r'\runf_for_vvwm_' + sfx_o
    bif_out = determ_dir + r'\bif_for_vvwm_' + sfx_o
    # logging.info("01b: Writing final data to <" + runf_out + "> and <" + bif_out + ">.")

    runf_msg = dask.delayed(save_and_finish)(runf_sub, runf_out)
    bif_msg = dask.delayed(save_and_finish)(bif_sub, bif_out)
    delayed_tasks.extend([runf_msg, bif_msg])

logging.info("01b: Getting the time series data for runoff rate and bifenthrin using swmmtoolbox's extract function.")
dask.delayed(print)(delayed_tasks).compute()

