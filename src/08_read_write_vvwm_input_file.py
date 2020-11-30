# -----------------------------------------
# read, write, VVWM input file
# -----------------------------------------

# setup
import shutil, os, pandas as pd
from path_names import dir_path, vvwm_path
from prpy_bookkeeping import *

# outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
#             '\outfall_31_36', '\outfall_31_38', '\outfall_31_42']
outfalls = ['outfall_31_26', 'outfall_31_28', 'outfall_31_29', 'outfall_31_35',
            'outfall_31_36', 'outfall_31_38', 'outfall_31_42']

# nsims
nsims = 5

# read in lhs_sampled_params
loginfo("Reading in lhs sampled parameters from <" + dir_path + "\io\lhs_sampled_params_vvwm.csv>.")
lhs_design = pd.read_csv(os.path.join(dir_path, "io", "lhs_sampled_params_vvwm.csv"))#dir_path+r'\io\lhs_sampled_params_vvwm.csv')

# round lhs decimals
lhs_design = lhs_design.round(
    {"kd": 2, "aer_aq": 0, "aer_aq_temp": 2, "anae_aq": 0, "anae_aq_temp": 2, "photo": 2, "rflat": 0, "hydro": 2, "sol": 4,
     "benthic_depth": 3, "porosity": 2, "bulk_density": 2, "froc2": 3, "doc2": 2, "bnmas": 3, "sused": 3, "chl": 3,
     "froc1": 3, "doc1": 2})
print(lhs_design.head())

# do the following for each outfall...replace inputs with lhs inputs
loginfo("Looping thru outfalls for navigating to each vwmm folder and then each of its " + str(nsims) + " input folders.")
for o in outfalls:

    # set pathways
    outfall_dir = os.path.join(vvwm_path, o)#vvwm_path + o

    # do for each simulation...
    loginfo("Looping thru simulations of " + o[1:] + " to replace inputs with lhs inputs.")
    for Ite in range(1, nsims + 1):

        # create new input folder for sim
        new_dir = os.path.join(outfall_dir, "input_" + str(Ite))#outfall_dir + r'\input_' + str(Ite)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
            print("Folder ", Ite, " created", "\n")
        else:
            print("Folder ", Ite, "already exists")

        # copy base file into new file location
        old_path = os.path.join(vvwm_path, "vvwmTransfer.txt")#vvwm_path + r'\vvwmTransfer.txt'
        new_path = os.path.join(new_dir, "vvwmTransfer.txt")#new_dir + r'\vvwmTransfer.txt'
        shutil.copyfile(old_path, new_path)

        # start reading the new file
        new_file = open(new_path, "r")
        filelines = new_file.readlines()
        new_file.close()

        # edit the new file
        # parameter = kd
        row_0 = 4
        var = lhs_design.loc[Ite - 1, "kd"]
        filelines[row_0] = str(var) + "\n"

        # parameter = aer_aq
        row_0 = 5
        var = lhs_design.loc[Ite - 1, "aer_aq"]
        filelines[row_0] = str(var) + "\n"

        # parameter = aer_aq_temp
        row_0 = 6
        var = lhs_design.loc[Ite - 1, "aer_aq_temp"]
        filelines[row_0] = str(var) + "\n"

        # parameter = anae_aq
        row_0 = 7
        var = lhs_design.loc[Ite - 1, "anae_aq"]
        filelines[row_0] = str(var) + "\n"

        # parameter = anae_aq_temp
        row_0 = 8
        var = lhs_design.loc[Ite - 1, "anae_aq_temp"]
        filelines[row_0] = str(var) + "\n"

        # parameter = photo
        row_0 = 9
        var = lhs_design.loc[Ite - 1, "photo"]
        filelines[row_0] = str(var) + "\n"

        # parameter = rflat
        row_0 = 10
        var = lhs_design.loc[Ite - 1, "rflat"]
        filelines[row_0] = str(var) + "\n"

        # parameter = hydro
        row_0 = 11
        var = lhs_design.loc[Ite - 1, "hydro"]
        filelines[row_0] = str(var) + "\n"

        # parameter = sol
        row_0 = 17
        var = lhs_design.loc[Ite - 1, "sol"]
        filelines[row_0] = str(var) + "\n"

        # parameter = benthic depth
        row_0 = 40
        var = lhs_design.loc[Ite - 1, "benthic_depth"]
        filelines[row_0] = str(var) + "\n"

        # parameter = porosity
        row_0 = 41
        var = lhs_design.loc[Ite - 1, "porosity"]
        filelines[row_0] = str(var) + "\n"

        # parameter = bulk_density
        row_0 = 42
        var = lhs_design.loc[Ite - 1, "bulk_density"]
        filelines[row_0] = str(var) + "\n"

        # parameter = froc2
        row_0 = 43
        var = lhs_design.loc[Ite - 1, "froc2"]
        filelines[row_0] = str(var) + "\n"

        # parameter = doc2
        row_0 = 44
        var = lhs_design.loc[Ite - 1, "doc2"]
        filelines[row_0] = str(var) + "\n"

        # parameter = bnmas
        row_0 = 45
        var = lhs_design.loc[Ite - 1, "bnmas"]
        filelines[row_0] = str(var) + "\n"

        # parameter = sused
        row_0 = 47
        var = lhs_design.loc[Ite - 1, "sused"]
        filelines[row_0] = str(var) + "\n"

        # parameter = chl
        row_0 = 48
        var = lhs_design.loc[Ite - 1, "chl"]
        filelines[row_0] = str(var) + "\n"

        # parameter = froc1
        row_0 = 49
        var = lhs_design.loc[Ite - 1, "froc1"]
        filelines[row_0] = str(var) + "\n"

        # parameter = doc1
        row_0 = 50
        var = lhs_design.loc[Ite - 1, "doc1"]
        filelines[row_0] = str(var) + "\n"

        # copy, write out file
        new_file = open(new_path, "w")
        new_file.writelines(filelines)
        new_file.close()
