

# ------------------------------------------------------------------------------------------
# read swmm .rpt output file, and store desired outputs
# ------------------------------------------------------------------------------------------

# setup
import pandas, os
from datetime import date

# specify locations
dir_path = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\probabilistic_python'

swmm_path = dir_path + r'\input\swmm'
print(swmm_path)
swmm_file = swmm_path + r'\NPlesantCreek.rpt'
print(swmm_file)
inp_file = swmm_path + r'\NPlesantCreek.inp'
print(inp_file)
vvwm_path = dir_path + r'\input\vvwm'
print(vvwm_path)

outfalls = ['\outfall_31_26']

# read in the .inp file subcatchment areas (to use later in script)
# read the .inp file
file = open(inp_file, "r")

# create blank list to hold subcatchment areas
sub_list_area = []

# skip x lines
lines1 = file.readlines()[58:]

for thissub in range(0, 113):
    # grab the area
    thisline = lines1[thissub]
    fixline = " ".join(thisline.split())
    listline = fixline.split()
    area = listline[3]
    area = float(area)

    # insert into blank list
    sub_list_area.append(area)

with open(r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\app_rates\swmm_sub_list_areas.txt', 'w') as f:
    for item in sub_list_area:
        f.write("%s\n" % item)


# read in .rpt values of runf and bif conc.
# time period
firstday = date(2009, 1, 2)
lastday = date(2017, 12, 31)
delta = lastday - firstday
days = delta.days
dates = pandas.date_range(firstday, lastday).tolist()

# create blank data frame
runf_df = pandas.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
bif_df = pandas.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)

# read the .rpt file
file = open(swmm_file, "r")

# for subcatchment 1
# create blank list to hold subcatchment's runoff, and bifenthrin concentration
sub_list_runf = []
sub_list_bif = []

# skip x lines to start at day1 for subcatchment1
lines1 = file.readlines()[60:]

for thisday in range(0, days + 1):
    # grab the runf value
    thisline = lines1[thisday]
    fixline = " ".join(thisline.split())
    listline = fixline.split()
    runf = listline[4]
    bif = listline[7]

    # insert into blank list
    sub_list_runf.append(runf)
    sub_list_bif.append(bif)

# insert list into data frame col
runf_df[1, ] = sub_list_runf
runf_df.rename(columns={runf_df.columns[0]: '1'}, inplace=True)

bif_df[1, ] = sub_list_bif
bif_df.rename(columns={bif_df.columns[0]: '1'}, inplace=True)

# for subcatchment 2 - 113
for sub in range(2, 114):
    # skip lines to get to the next subcatchment's info
    file = open(swmm_file, "r")
    skipto = (59 + ((days + 9) * (sub - 1))) - (sub - 2)
    lines = file.readlines()[skipto:]

    # create blank list to hold subcatchment's runoff and bifenthrin concentration
    sub_list_runf = []
    sub_list_bif = []

    for thisday in range(0, days + 1):
        # grab the runf value
        thisline = lines[thisday]
        fixline = " ".join(thisline.split())
        listline = fixline.split()

        # if/then for entries whose bif conc is so large that it bleeds into the preceding column
        if len(listline) == 7:
            runf = listline[4]

            # 2 smooshed cols
            bug = listline[6]

            # find the first instance of a decimal point
            dist = bug.find('.')

            # scan over 5 characters -> (rounding length for this col)
            bug_scan = dist + 5

            # chop string at this location
            bif = bug[bug_scan:]
            print(bif)

        elif len(listline) == 8:
            runf = listline[4]
            bif = listline[7]

        # insert into blank list
        sub_list_runf.append(runf)
        sub_list_bif.append(bif)

    # insert list into data frame col
    runf_df[sub, ] = sub_list_runf
    bif_df[sub, ] = sub_list_bif

    # rename column names
    runf_df.rename(columns={runf_df.columns[sub - 1]: str(sub)}, inplace=True)
    bif_df.rename(columns={bif_df.columns[sub - 1]: str(sub)}, inplace=True)

# convert values from object to float
for columnName in runf_df.columns:
    runf_df[columnName] = runf_df[columnName].astype(float)
for columnName in bif_df.columns:
    bif_df[columnName] = bif_df[columnName].astype(float)

# read out runf_df and bif_df
runf_out = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\app_rates\swmm_output_runf.csv'
runf_df.to_csv(runf_out)
bif_out = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\app_rates\swmm_output_bif.csv'
bif_df.to_csv(bif_out)

# copy
runf_conv = runf_df
bif_conv = bif_df

# specify loop variables
runf_df_cols = len(runf_conv.columns)
runf_df_rows = len(runf_conv)
bif_df_cols = len(bif_conv.columns)
bif_df_rows = len(bif_conv)

# conversion for runf
for c in range(0, runf_df_cols):

    # define subcatchment's area
    this_area = sub_list_area[c]

    for r in range(0, runf_df_rows):
        # compute cm/ha/day
        runf_conv.iloc[r, c] = (runf_conv.iloc[r, c] * 86400) / this_area

runf_conv_out = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\app_rates\swmm_runf_conv_for_vvwm.csv'
runf_conv.to_csv(runf_conv_out)

# conversion for bifenthrin conc.
for c in range(0, bif_df_cols):

    # define subcatchment's area
    this_area = sub_list_area[c]

    for r in range(0, bif_df_rows):
        # define the runoff value (m3/day)
        this_runf = runf_df.iloc[r, c] * 864000

        # compute g/ha/day
        bif_conv.iloc[r, c] = (bif_conv.iloc[r, c] * 1000 * this_runf) / (1.0e6 * this_area)

bif_conv_out = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\app_rates\swmm_bif_conv_for_vvwm.csv'
bif_conv.to_csv(bif_conv_out)

# subset subcatchment outputs for each vvwm
for o in outfalls:
    # set pathways
    outfall_path = vvwm_path + o
    determ_inputs = outfall_path + r'\determ'
    outfall_file = outfall_path + o + r'.csv'

    # declare which columns need to be subset
    sub_file = pandas.read_csv(outfall_file)
    sublist = sub_file['Subcatchment_ID'].tolist()

    collist = [x - 1 for x in sublist]  # columns to subset from df

    # subset
    runf_sub = runf_conv.iloc[:, collist]
    bif_sub = bif_conv.iloc[:, collist]

    # add a total sum column
    runf_sub["runf_sum"] = runf_sub.sum(axis=1)
    bif_sub["bif_sum"] = bif_sub.sum(axis=1)

    # add a date column
    runf_sub['date'] = pandas.date_range(start='1/2/2009', periods=len(runf_sub), freq='D')
    bif_sub['date'] = pandas.date_range(start='1/2/2009', periods=len(bif_sub), freq='D')

    # separate date column too
    runf_sub['year'] = runf_sub['date'].dt.year
    runf_sub['month'] = runf_sub['date'].dt.month
    runf_sub['day'] = runf_sub['date'].dt.day

    bif_sub['year'] = bif_sub['date'].dt.year
    bif_sub['month'] = bif_sub['date'].dt.month
    bif_sub['day'] = bif_sub['date'].dt.day

    # write out dataframes
    substring = outfall_file[102: 111:]
    runf_out = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\app_rates\runf_inputs_for_vvwm_' + substring
    bif_out = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\app_rates\bif_inputs_for_vvwm_' + substring
    runf_sub.to_csv(runf_out)
    bif_sub.to_csv(bif_out)

