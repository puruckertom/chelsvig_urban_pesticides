# ------------------------------------------------------------------------------------------
# read SWMM .rpt output file, and store desired outputs
# ------------------------------------------------------------------------------------------

# setup
import pandas as pd, os, numpy as np
from datetime import date

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

# nsims
nsims = 5

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
        print("Folder ", Ite, " created", "\n")
    else:
        print("Folder ", Ite, "already exists")
    os.getcwd()
    os.chdir(newdir)

    # read in the .inp file subcatchment areas (to use later in script)
    for rpt in range(1, nsims+1):
        folder_path = input_path + str(rpt)

        # read the .inp file
        inp_file = folder_path + r'\NPlesantCreek.inp'
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

        # read in .rpt values of runf and bif conc.
        # time period
        firstday = date(2009, 1, 2)
        lastday = date(2017, 12, 31)
        delta = lastday - firstday
        days = delta.days
        dates = pd.date_range(firstday, lastday).tolist()

        # create col names for data frame
        cols_list = []
        for s in range(1, 114):
            cols_list.insert(s - 1, "sub_" + str(s))

        # create blank data frame
        runf_df = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
        bif_df = pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)

        # read the .rpt file
        swmm_file = folder_path + r'\NPlesantCreek.rpt'
        file = open(swmm_file, "r")

        # for subcatchment 1
        # create blank list to hold subcatchment's runoff, and bifenthrin concentration
        sub_list_runf = []
        sub_list_bif = []

        # skip x lines to start at day1 for subcatchment1
        lines1 = file.readlines()[57:]

        for thisday in range(0, days+1):
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
        runf_df['sub_1'] = np.array(sub_list_runf)
        bif_df['sub_1'] = np.array(sub_list_bif)

        # for subcatchment 2 - 113
        for sub in range(2, 114):
            # skip lines to get to the next subcatchment's info
            file = open(swmm_file, "r")
            skipto = (56 + ((days + 9) * (sub - 1))) - (sub - 2)
            lines = file.readlines()[skipto:]

            # create blank list to hold subcatchment's runoff and bifenthrin concentration
            sub_list_runf = []
            sub_list_bif = []

            for thisday in range(0, days+1):
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
            runf_df['sub_' + str(sub)] = np.array(sub_list_runf)
            bif_df['sub_' + str(sub)] = np.array(sub_list_bif)

        # convert values from object to float
        for columnName in runf_df.columns:
            runf_df[columnName] = runf_df[columnName].astype(float)
        for columnName in bif_df.columns:
            bif_df[columnName] = bif_df[columnName].astype(float)

        # copy
        runf_conv = runf_df.copy()
        bif_conv = bif_df.copy()

        # specify loop variables
        runf_df_cols = len(runf_conv.columns)
        runf_df_rows = len(runf_conv)
        bif_df_cols = len(bif_conv.columns)
        bif_df_rows = len(bif_conv)

        # conversion for runf
        for c in range(0, runf_df_cols):
            col_name = "sub_" + str(c + 1)

            # define subcatchment's area
            this_area = sub_list_area[c]

            # perform conversion (cm/ha/day)
            runf_conv[col_name] = (runf_conv[col_name] * 86400 * 0.01) / this_area

        # conversion for bifenthrin conc.
        for c in range(0, bif_df_cols):

            # define subcatchment's area
            this_area = sub_list_area[c]

            for r in range(0, bif_df_rows):
                # define the runoff value (m3/day)
                this_runf = runf_df.iloc[r, c] * 864000

                # compute g/ha/day
                bif_conv.iloc[r, c] = ((bif_conv.iloc[r, c]) * 1000 * this_runf) / (1.0e6 * this_area)

        # subset subcatchment outputs for each vvwm
        outfall_file = outfall_path + '\\' + o + r'.csv'

        # declare which columns need to be subset
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
        runf_sub['date'] = pd.date_range(start='1/2/2009', periods=len(runf_sub), freq='D')
        bif_sub['date'] = pd.date_range(start='1/2/2009', periods=len(bif_sub), freq='D')

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
        runf_out = out_folder + r'\runf_' + substring
        bif_out = out_folder + r'\bif_' + substring
        runf_sub.to_csv(runf_out)
        bif_sub.to_csv(bif_out)


