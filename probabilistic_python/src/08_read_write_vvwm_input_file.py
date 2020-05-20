# -----------------------------------------
# read, write, VVWM input file
# -----------------------------------------

# setup
import shutil, os, pandas

# specify location
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

input_path = dir_path + r'\input\vvwm'
print(input_path)

# nsims
nsims = 5

# read in lhs_sampled_params
lhs_design = pandas.read_csv(dir_path+r'\io\lhs_sampled_params_vvwm.csv')

# todo - the below code has NOT been altered since copy-paste from swmm script

# round lhs decimals
lhs_design = lhs_design.round(
    {"NImperv": 4, "NPerv": 4, "SImperv":3, "SPerv": 3, "PctZero": 3, "MaxRate": 3, "MinRate": 3, "Decay": 2, "DryTime": 0,
     "Por": 3, "WP": 3, "FC": 3, "Ksat": 3, "Rough": 4, "Kdecay": 3, "BCoeff2": 3, "WCoeff2": 3})
print(lhs_design.head())

# do the following for each simulation...
for Ite in range(1, nsims+1):
    newfol = "input_" + str(Ite)
    print(newfol)

    newdir = os.path.join(input_path, newfol)

    if not os.path.exists(newdir):
        os.mkdir(newdir)
        print("Folder ", Ite, " created", "\n")
    else:
        print("Folder ", Ite, "already exists")

    os.getcwd()
    os.chdir(newdir)

    # copy base file into new file location
    old_swmm5 = os.path.join(input_path, "NPlesantCreek.inp")
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
        listline = fixline.split()
        listline[1] = str(NImperv)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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

        fixline = " ".join(oldline.split())
        listline = fixline.split()
        listline[2] = str(NPerv)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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

        fixline = " ".join(oldline.split())
        listline = fixline.split()
        listline[3] = str(SImperv)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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

        fixline = " ".join(oldline.split())
        listline = fixline.split()
        listline[4] = str(SPerv)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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

        fixline = " ".join(oldline.split())
        listline = fixline.split()
        listline[5] = str(PctZero)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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
        listline = fixline.split()
        listline[1] = str(MaxRate)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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

        fixline = " ".join(oldline.split())
        listline = fixline.split()
        listline[2] = str(MinRate)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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

        fixline = " ".join(oldline.split())
        listline = fixline.split()
        listline[3] = str(Decay)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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

        fixline = " ".join(oldline.split())
        listline = fixline.split()
        listline[4] = str(DryTime)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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
        listline = fixline.split()
        listline[1] = str(Por)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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

        fixline = " ".join(oldline.split())
        listline = fixline.split()
        listline[2] = str(WP)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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

        fixline = " ".join(oldline.split())
        listline = fixline.split()
        listline[3] = str(FC)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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

        fixline = " ".join(oldline.split())
        listline = fixline.split()
        listline[4] = str(Ksat)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
        filelines[row_t] = newline

    # # ---------------------------
    # # parameter = Rough
    # # ---------------------------
    # Num = 195  # number of conduits
    # row_0 = 734
    # Rough = lhs_design.loc[Ite - 1, "Rough"]
    # print(Rough)
    #
    # for i in range(1, Num + 1):
    #     row_t = row_0 + (i - 1)
    #     oldline = filelines[row_t]
    #
    #     fixline = " ".join(oldline.split())
    #     listline = fixline.split()
    #     listline[4] = str(Rough)
    #     listTOstring = ' '.join([str(item) for item in listline])
    #
    #     newline = listTOstring + "\n"
    #     filelines[row_t] = newline

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
        listline = fixline.split()
        listline[5] = str(Kdecay)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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
        listline = fixline.split()
        listline[4] = str(BCoeff2)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
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
        listline = fixline.split()
        listline[4] = str(WCoeff2)
        listTOstring = ' '.join([str(item) for item in listline])

        newline = listTOstring + "\n"
        filelines[row_t] = newline


    # copy, write out file
    new_swmm5 = open(new_file, "w")
    new_swmm5.writelines(filelines)
    new_swmm5.close()

