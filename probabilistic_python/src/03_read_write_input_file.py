# -----------------------------------------
# read, write, input file
# -----------------------------------------

import pytest_shutil, shutil, os, pandas, regex as re

# nsims
nsims = 5

# define root path for all folders
root_path = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\probabilistic_python\input\swmm'
print(os.path.exists(root_path))

# read in lhs_sampled_params
lhs_design = pandas.read_csv(
    r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\probabilistic_python\io\lhs_sampled_params.csv')

# round lhs decimals
lhs_design = lhs_design.round(
    {"NImperv": 4, "NPerv": 4, "SImperv":3, "SPerv": 3, "PctZero": 3, "MaxRate": 3, "MinRate": 3, "Decay": 2, "DryTime": 0,
     "Por": 3, "WP": 3, "FC": 3, "Ksat": 3, "Roughness": 4, "Kdecay": 3, "BCoeff2": 3, "WCoeff2": 3})
print(lhs_design.head())

# do the following for each simulation...
for Ite in range(1, nsims+1):
    newfol = "input_" + str(Ite)
    print(newfol)

    newdir = os.path.join(root_path, newfol)
    print(newdir)

    if not os.path.exists(newdir):
        os.mkdir(newdir)
        print("Folder ", Ite, " created", "\n")
    else:
        print("Folder ", Ite, "already exists")

    os.getcwd()
    os.chdir(newdir)

    # copy base file into new file location
    old_swmm5 = os.path.join(root_path, "NPlesantCreek.inp")
    new_file = os.path.join(newdir, "NPlesantCreek.inp")
    shutil.copyfile(old_swmm5, new_file)

    # start reading the new file
    new_swmm5 = open(new_file, "r")
    filelines = new_swmm5.readlines()

    # edit the new file
    # ---------------------------
    # parameter = NImperv
    # ---------------------------
    Num = 113  # number of subcatchments
    row_0 = 175
    NImperv = lhs_design.loc[Ite - 1, "NImperv"]
    print(NImperv)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        fixline = " ".join(oldline.split())
        newline = re.sub(r'\b0.013\b', str(NImperv), fixline)
        newline = newline + "\n"
        filelines[row_t] = newline

    # ---------------------------
    # parameter = NPerv
    # ---------------------------
    Num = 113  # number of subcatchments
    row_0 = 175
    NPerv = lhs_design.loc[Ite - 1, "NPerv"]
    print(NPerv)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        newline = re.sub(r'\b0.15\b', str(NPerv), oldline)
        filelines[row_t] = newline

    # ---------------------------
    # parameter = SImperv
    # ---------------------------
    Num = 113  # number of subcatchments
    row_0 = 175
    SImperv = lhs_design.loc[Ite - 1, "SImperv"]
    print(SImperv)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        newline = re.sub(r'\b2.54\b', str(SImperv), oldline)
        filelines[row_t] = newline

    # ---------------------------
    # parameter = SPerv
    # ---------------------------
    Num = 113  # number of subcatchments
    row_0 = 175
    SPerv = lhs_design.loc[Ite - 1, "SPerv"]
    print(SPerv)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        newline = re.sub(r'\b5.08\b', str(SPerv), oldline)
        filelines[row_t] = newline

    # ---------------------------
    # parameter = PctZero
    # ---------------------------
    Num = 113  # number of subcatchments
    row_0 = 175
    PctZero = lhs_design.loc[Ite - 1, "PctZero"]
    print(PctZero)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        newline = re.sub(r'\b17\b', str(PctZero), oldline)
        filelines[row_t] = newline

    # ---------------------------
    # parameter = MaxRate
    # ---------------------------
    Num = 113  # number of subcatchments
    row_0 = 292
    MaxRate = lhs_design.loc[Ite - 1, "MaxRate"]
    print(MaxRate)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        fixline = " ".join(oldline.split())
        newline = re.sub(r'\b79\b', str(MaxRate), fixline)
        newline = newline + "\n"
        filelines[row_t] = newline

    # ---------------------------
    # parameter = MinRate
    # ---------------------------
    Num = 113  # number of subcatchments
    row_0 = 292
    MinRate = lhs_design.loc[Ite - 1, "MinRate"]
    print(MinRate)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        newline = re.sub(r'\b1.3\b', str(MinRate), oldline)
        filelines[row_t] = newline

    # ---------------------------
    # parameter = Decay
    # ---------------------------
    Num = 113  # number of subcatchments
    row_0 = 292
    Decay = lhs_design.loc[Ite - 1, "Decay"]
    print(Decay)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        newline = re.sub(r'\b4.14\b', str(Decay), oldline)
        filelines[row_t] = newline

    # ---------------------------
    # parameter = DryTime
    # ---------------------------
    Num = 113  # number of subcatchments
    row_0 = 292
    DryTime = lhs_design.loc[Ite - 1, "DryTime"]
    print(DryTime)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        newline = re.sub(r'\b7\b', str(DryTime), oldline)
        filelines[row_t] = newline

    # ---------------------------
    # parameter = Por
    # ---------------------------
    Num = 1  # number of aquifers
    row_0 = 409
    Por = lhs_design.loc[Ite - 1, "Por"]
    print(Por)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        fixline = " ".join(oldline.split())
        newline = re.sub(r'\b0.5\b', str(Por), fixline)
        newline = newline + "\n"
        filelines[row_t] = newline

    # ---------------------------
    #   parameter = WP
    # ---------------------------
    Num = 1  # number of aquifers
    row_0 = 409
    WP = lhs_design.loc[Ite - 1, "WP"]
    print(WP)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        newline = re.sub(r'\b0.15\b', str(WP), oldline)
        filelines[row_t] = newline

    # ---------------------------
    # parameter = FC
    # ---------------------------
    Num = 1  # number of aquifers
    row_0 = 409
    FC = lhs_design.loc[Ite - 1, "FC"]
    print(FC)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        newline = re.sub(r'\b0.30\b', str(FC), oldline)
        filelines[row_t] = newline

    # ---------------------------
    # parameter = Ksat
    # ---------------------------
    Num = 1  # number of aquifers
    row_0 = 409
    Ksat = lhs_design.loc[Ite - 1, "Ksat"]
    print(Ksat)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        newline = re.sub(r'\b4.9\b', str(Ksat), oldline)
        filelines[row_t] = newline

    # ---------------------------
    # parameter = Roughness
    # ---------------------------
    Num = 195  # number of conduits
    row_0 = 734
    Roughness = lhs_design.loc[Ite - 1, "Roughness"]
    print(Roughness)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        fixline = " ".join(oldline.split())
        newline = re.sub(r'\b0.014\b', str(Roughness), fixline)
        newline2 = re.sub(r'\b0.01\b', str(Roughness), newline)
        newline2 = newline2 + "\n"
        filelines[row_t] = newline2

    # ---------------------------
    # parameter = Kdecay
    # ---------------------------
    Num = 1  # number of pollutants
    row_0 = 1128
    Kdecay = lhs_design.loc[Ite - 1, "Kdecay"]
    print(Kdecay)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        fixline = " ".join(oldline.split())
        newline = re.sub(r'\b0.004283931\b', str(Kdecay), fixline)
        newline = newline + "\n"
        filelines[row_t] = newline

    # ---------------------------
    # parameter = BCoeff2
    # ---------------------------
    Num = 1  # number of pollutants
    row_0 = 1374
    BCoeff2 = lhs_design.loc[Ite - 1, "BCoeff2"]
    print(BCoeff2)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        fixline = " ".join(oldline.split())
        newline = fixline.replace("1.0", str(BCoeff2))
        newline = re.sub(r'\b1.0\b', str(BCoeff2), fixline)
        newline = newline + "\n"
        filelines[row_t] = newline

    # ---------------------------
    # parameter = WCoeff2
    # ---------------------------
    Num = 1  # number of pollutants
    row_0 = 1380
    WCoeff2 = lhs_design.loc[Ite - 1, "WCoeff2"]
    print(WCoeff2)

    for i in range(1, Num + 1):
        row_t = row_0 + (i - 1)
        oldline = filelines[row_t]

        fixline = " ".join(oldline.split())
        newline = re.sub(r'\b1.0\b', str(WCoeff2), fixline)
        newline = newline + "\n"
        filelines[row_t] = newline


    # copy, write out file
    new_swmm5 = open(new_file, "w")
    new_swmm5.writelines(filelines)
    new_swmm5.close()

# ----------------------------------------------
# the end
# ----------------------------------------------
