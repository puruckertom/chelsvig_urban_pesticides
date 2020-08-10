# ------------------------------------------------------------------------------------------
# read swmm .out binary file, and store desired outputs
# ------------------------------------------------------------------------------------------

# setup
import pandas as pd, os, numpy as np
import swmmtoolbox.swmmtoolbox as swmmtoolbox
from datetime import date

# specify locations
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

swmm_path = dir_path + r'\input\swmm'
print(swmm_path)
bin_file = swmm_path + r'\NPlesantCreek.out'
print(bin_file)
inp_file = swmm_path + r'\NPlesantCreek.inp'
print(inp_file)
vvwm_path = dir_path + r'\input\vvwm'
print(vvwm_path)

outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42',]

# displays version number and system info
# swmmtoolbox.about()

# list the catalog of objects in .out file (lists all available labels for extract function
# swmmtoolbox.catalog(filename, itemtype='', header='default')

# list variables available for each type (shows variable name and its index)
# use this info for 'extract' function's 'var' parameter
# swmmtoolbox.listvariables(filename, header='default')

# get the time series data for a particular object and variable
# swmmtoolbox.extract(filename, *labels)
# labels = 'type,name,var'
# labels require two commas and no spaces
# use 'catalog' and 'listvariables' for var parameters
# there is a wild card feature for labels, where leaving the part out
#   will return all labels that match all other parts.
lab1 = 'subcatchment,,Runoff_rate'
lab2 = 'subcatchment,,Bifenthrin'
extract_runf = swmmtoolbox.extract(bin_file, lab1)
extract_bif = swmmtoolbox.extract(bin_file, lab2)

# write out swmm outputs
extract_runf.to_csv(swmm_path + r'\swmm_output_runf.csv')
extract_bif.to_csv(swmm_path + r'\swmm_output_bif.csv')

# read file back in, remove date/time col
swmmout_runf = pd.read_csv(swmm_path + r'\swmm_output_runf.csv')
swmmout_runf = swmmout_runf.drop(['Unnamed: 0'], axis=1)
swmmout_bif = pd.read_csv(swmm_path + r'\swmm_output_bif.csv')
swmmout_bif = swmmout_bif.drop(['Unnamed: 0'], axis=1)

# copy
runf_to_conv = swmmout_runf.copy()
bif_to_conv = swmmout_bif.copy()

# specify loop variables
runf_df_cols = len(runf_to_conv.columns)  # 113
runf_df_rows = len(runf_to_conv)  # 78887
bif_df_cols = len(bif_to_conv.columns)
bif_df_rows = len(bif_to_conv)

# read in the .inp file subcatchment areas
file = open(inp_file, "r")
# create blank list to hold subcatchment areas
sub_list_area = []
# skip x lines
lines1 = file.readlines()[55:]
for thissub in range(0, 113):
    # grab the area
    thisline = lines1[thissub]
    fixline = " ".join(thisline.split())
    listline = fixline.split()
    area = listline[3]
    area = float(area)
    # insert into blank list
    sub_list_area.append(area)

# conversion for runf
for c in range(0, runf_df_cols):
    col_name = "subcatchment_S" + str(c + 1) + "_Runoff_rate"
    # define subcatchment's area
    this_area = sub_list_area[c]
    # perform conversion
    runf_to_conv[col_name] = (runf_to_conv[col_name] * 86400 * 0.01) / this_area

# conversion for bifenthrin conc.
for c in range(0, bif_df_cols):
    # define subcatchment's area
    this_area = sub_list_area[c]
    for r in range(0, bif_df_rows):
        # define the runoff value (m3/day)
        this_runf = swmmout_runf.iloc[r, c] * 864000
        # compute g/ha/day
        bif_to_conv.iloc[r, c] = ((bif_to_conv.iloc[r, c]) * 1000 * this_runf) / (1.0e6 * this_area)

# subset subcatchment outputs for each vvwm
for o in outfalls:
    # set pathways
    outfall_path = vvwm_path + o
    determ_inputs = outfall_path + r'\determ'
    outfall_file = outfall_path + o + r'.csv'

    # declare which columns need to be subset for the respective outfall
    sub_file = pd.read_csv(outfall_file)
    sublist = sub_file['Subcatchment_ID'].tolist()

    collist = [x - 1 for x in sublist]  # columns to subset from df

    # subset
    runf_sub = runf_conv.iloc[:, collist]
    bif_sub = bif_conv.iloc[:, collist]

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
    substring = outfall_file[102: 111:]
    runf_out = determ_inputs + r'\runf_' + substring
    bif_out = determ_inputs + r'\bif_' + substring
    runf_sub.to_csv(runf_out)
    bif_sub.to_csv(bif_out)