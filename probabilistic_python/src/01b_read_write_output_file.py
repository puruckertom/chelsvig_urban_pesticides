# ------------------------------------------------------------------------------------------
# read swmm .rpt output file, and store desired outputs
# ------------------------------------------------------------------------------------------

# setup
import pandas, os
from datetime import date

# specify location
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

input_path = dir_path + r'\input\swmm'
print(input_path)
file_path = input_path + r'\NPlesantCreek.rpt'
print(file_path)

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
file = open(file_path, "r")

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
runf_df.rename(columns={runf_df.columns[0]: 'sub_1'}, inplace=True)

bif_df[1, ] = sub_list_bif
bif_df.rename(columns={bif_df.columns[0]: 'sub_1'}, inplace=True)

# for subcatchment 2 - 113
for sub in range(2, 114):
    # skip lines to get to the next subcatchment's info
    file = open(file_path, "r")
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
    runf_df.rename(columns={runf_df.columns[sub - 1]: 'sub_' + str(sub)}, inplace=True)
    bif_df.rename(columns={bif_df.columns[sub - 1]: 'sub_' + str(sub)}, inplace=True)

# see what output looks like
print(runf_df)
print(bif_df)

# add a total sum column
#todo need to fix this code...not summing correctly
runf_df["runf_sum"] = runf_df.sum(axis=1)
bif_df["bif_sum"] = bif_df.sum(axis=1)

# add a date column
runf_df['date'] = pandas.date_range(start='1/3/2009', periods=len(runf_df), freq='D')
bif_df['date'] = pandas.date_range(start='1/3/2009', periods=len(bif_df), freq='D')

# write out dataframes
runf_out = input_path + r'\subcatchment_runf.csv'
bif_out = input_path + r'\subcatchment_bif.csv'
runf_df.to_csv(runf_out)
bif_df.to_csv(bif_out)
