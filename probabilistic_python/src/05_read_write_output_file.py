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

input_path = dir_path + r'\input\swmm\input_'
print(input_path)

# nsims
nsims = 5

# time period
firstday = date(2009, 1, 2)
lastday = date(2009, 12, 31)
delta = lastday - firstday
days = delta.days

# read in the .rpt file for each simulation
for rpt in range(1, nsims+1):
    folder_path = input_path + str(rpt)
    file_path = folder_path + r'\NPlesantCreek.rpt'
    print(file_path)

    # create blank data frame
    runf_df = pandas.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)

    # read the .rpt file
    file = open(file_path, "r")

    # for subcatchment 1
    # create blank list to hold subcatchment's runf values
    sub_list = []

    # skip x lines to start at day1 for subcatchment1
    lines1 = file.readlines()[60:]

    for thisday in range(0, days):
        # grab the runf value
        thisline = lines1[thisday]
        fixline = " ".join(thisline.split())
        listline = fixline.split()
        runf = listline[4]

        # insert into blank list
        sub_list.append(runf)

    # insert list into data frame col
    runf_df[1, ] = sub_list
    runf_df.rename(columns={runf_df.columns[0]: 'sub_1'}, inplace=True)

    # for subcatchment 2 - 113
    for sub in range(2, 114):
        # skip lines to get to the next subcatchment's info
        file = open(file_path, "r")
        skipto = (60 + ((days + 9) * (sub - 1))) - (sub - 2)
        lines = file.readlines()[skipto:]

        # create blank list to hold subcatchment's runf values
        sub_list = []

        for thisday in range(0, days):
            # grab the runf value
            thisline = lines[thisday]
            fixline = " ".join(thisline.split())
            listline = fixline.split()
            runf = listline[4]

            # insert into blank list
            sub_list.append(runf)

        # insert list into data frame col
        runf_df[sub, ] = sub_list

        # rename column names
        runf_df.rename(columns={runf_df.columns[sub - 1]: 'sub_' + str(sub)}, inplace=True)

    # see what output looks like
    print(runf_df)

# todo rename rows with date
# todo add column that sums across the rows
# todo write out the entire data frame
# todo write out just the date and total_runf columns
# todo do the same for the concentration of bifenthrin variable