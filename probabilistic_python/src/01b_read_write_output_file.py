# ------------------------------------------------------------------------------------------
# read swmm .rpt output file, and store desired outputs
# ------------------------------------------------------------------------------------------

# setup
import pandas, os
from datetime import date

# specify locations
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

swmm_path = dir_path + r'\input\swmm'
print(swmm_path)
swmm_file = swmm_path + r'\NPlesantCreek.rpt'
print(swmm_file)
vvwm_path = dir_path + r'\input\vvwm'
print(vvwm_path)

outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42',]

# time period
firstday = date(2009, 1, 2)
lastday = date(2009, 12, 31)
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

for thisday in range(0, days):
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
    skipto = (60 + ((days + 9) * (sub - 1))) - (sub - 2)
    lines = file.readlines()[skipto:]

    # create blank list to hold subcatchment's runoff and bifenthrin concentration
    sub_list_runf = []
    sub_list_bif = []

    for thisday in range(0, days):
        # grab the runf value
        thisline = lines[thisday]
        fixline = " ".join(thisline.split())
        listline = fixline.split()
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

# subset subcatchment outputs for each vvwm
for o in outfalls:
    # set pathways
    outfall_path = vvwm_path + o
    determ_inputs = outfall_path + r'\inputs\determ'
    outfall_file = outfall_path + o + r'.csv'

    # declare which columns need to be subset
    sub_file = pandas.read_csv(outfall_file)
    sublist = sub_file['Subcatchment_ID'].tolist()

    collist = [x - 1 for x in sublist]  # columns to subset from df

    # subset
    runf_sub = runf_df.iloc[:, collist]
    bif_sub = bif_df.iloc[:, collist]

    # add a total sum column
    runf_sub["runf_sum"] = runf_sub.sum(axis=1)
    bif_sub["bif_sum"] = bif_sub.sum(axis=1)

    # add a date column
    runf_sub['date'] = pandas.date_range(start='1/3/2009', periods=len(runf_sub), freq='D')
    bif_sub['date'] = pandas.date_range(start='1/3/2009', periods=len(bif_sub), freq='D')

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
