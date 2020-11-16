# -----------------------------------------
# read, write, SWMM input file
# -----------------------------------------

# setup
import pytest_shutil, shutil, os, pandas as pd, regex as re
from path_names import main_path, dir_path, swmm_path
from prpy_bookkeeping import *

# nsims
nsims = 5

# read in lhs_sampled_params
loginfo("Reading in data from file <" + dir_path + r'\io\lhs_sampled_params.csv>.')
lhs_design = pd.read_csv(dir_path+r'\io\lhs_sampled_params.csv')
del (lhs_design['Unnamed: 0'])

# round lhs decimals
lhs_design = lhs_design.round(
    {"NImperv": 4, "NPerv": 4, "SImperv":3, "SPerv": 3, "PctZero": 3, "MaxRate": 3, "MinRate": 3, "Decay": 2, "DryTime": 0,
     "Por": 3, "WP": 3, "FC": 3, "Ksat": 3, "Rough": 4, "Kdecay": 3, "BCoeff2": 3, "WCoeff2": 3})
print(lhs_design.head())

'''
Helper function of edit_file:
Create new line of .inp file with lhs simulated versions of values and text in old .inp file
 Inputs: fileline <str> -line from original .inp file-
   Col <int> -column in the .inp file that contains the info you want to preserve and clean- 
   sim <float> -the simulated value to repace the old (observed) one with-
 Output: newline <str> -custom version of line for new file-
'''
def edit1line(fileline, Col, sim):
    listline = fileline.split()
    listline[Col] = str(sim)
    newline = ' '.join([str(item) for item in listline]) + "\n"
    return(newline)

'''
Edit the new file to be cleaner
 Inputs: Ite <int> -index of current simulation-
   Num <int> -Number of rows to clean-
   row_0 <int> -Number of rows to skip-
   parameter <str> -name of lhs design parameter (will become name of column in the .csv  file)-
   Col <int> -column in the .inp file that contains the info you want to preserve and clean- 
   flines <list of str> -lines of the file to clean up-
 Output: cleaned up lines of file given
'''
def editted_lines(Ite, Num, row_0, parameter, Col, flines):
    # value of "parameter" in current lhs simulation
    sim = lhs_design.loc[Ite - 1, parameter]
    print(sim)
    return([edit1line(flines[row_0 + i], Col, sim) for i in range(Num)])


# do the following for each simulation...
for Ite in range(1, nsims+1):
    loginfo("Simmulation " + str(Ite) + " of " + str(nsims))
    new_dir = swmm_path + r'\input_' + str(Ite)

    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
        print("Folder ", Ite, " created", "\n")
    else:
        print("Folder ", Ite, "already exists")

    # copy base file into new file location
    old_path = os.path.join(swmm_path, "NPlesantCreek.inp")
    new_path = os.path.join(new_dir, "NPlesantCreek.inp")
    loginfo("Copying base swmm input file <" + old_path + "> into <" + new_dir + ">.")
    shutil.copyfile(old_path, new_path)

    # start reading the new file
    loginfo("Opening file <" + new_path + "> to read.")
    new_file = open(new_path, "r")
    filelines = new_file.readlines()
    loginfo("Closing file <" + new_path + "> after reading lines into list.")
    new_file.close()

    # edit the new file

    # -----------------------------
    # first we need to correct some absolute paths, because they are currently only set to work on the author's computer
    filelines = replace_infile_abspaths(filelines = filelines)

    # # the first absolute path to correct, listified
    # path1cols = filelines[50].split()
    # # remember, there might be a space in the filepath, meaning that the split function could have created two elements, not 1
    # # so instead, make a new list using the first five, a space holder, and the last two elements of the original list
    # path1cols = path1cols[:5] + [""] + path1cols[-2:]
    # # the corrected element of the listified line
    # path1cols[5] = '"'+os.path.join(dir_path,"weather\swmm_wet.txt")+'"'
    # # insert the correction and unlistify!
    # filelines[50] = "\t".join(path1cols) + "\n"

    # # the second absolute path to correct, listified
    # path2cols = filelines[1384].split()
    # # remember, there might be a space in the filepath, meaning that the split function could have created two elements, not 1
    # # so instead, make a new list using the first 2 elements of the original list and a space holder
    # path2cols = path2cols[:2] + [""]
    # # the corrected element of the listified line
    # path2cols[2] = '"'+os.path.join(main_path,"app_rates\\calpip\\app_rate_output_for_swmm_48rain.txt")+'"'
    # # insert the correction and unlistify!
    # filelines[1384] = "\t".join(path2cols) + "\n"
    
    # # the third absolute path to correct, listified
    # path3cols = filelines[9306].split()
    # # remember, there might be a space in the filepath, meaning that the split function could have created two elements, not 1
    # # so instead, make a new list using the first element of the original list and a space holder
    # path3cols = path3cols[:1] + [""]
    # # the corrected element of the listified line
    # path3cols[1] = '"'+os.path.join(main_path,"probabilistic_python\\input\\swmm\\nplesant.jpg")+'"'
    # # insert the correction and unlistify!
    # filelines[9306] = "\t".join(path3cols) + "\n"

    # ---------------------------
    # 113 = number of subcatchments
    
    # parameter = NImperv
    filelines[172:(172 + 113)] = editted_lines(Ite = Ite, Num = 113, row_0 = 172, parameter = "NImperv", Col = 1, flines = filelines)
    
    # parameter = NPerv
    filelines[172:(172 + 113)] = editted_lines(Ite = Ite, Num = 113, row_0 = 172, parameter = "NPerv", Col = 2, flines = filelines)
    
    # parameter = SImperv
    filelines[172:(172 + 113)] = editted_lines(Ite = Ite, Num = 113, row_0 = 172, parameter = "SImperv", Col = 3, flines = filelines)

    # parameter = SPerv
    filelines[172:(172 + 113)] = editted_lines(Ite = Ite, Num = 113, row_0 = 172, parameter = "SPerv", Col = 4, flines = filelines)

    # parameter = PctZero
    filelines[172:(172 + 113)] = editted_lines(Ite = Ite, Num = 113, row_0 = 172, parameter = "PctZero", Col = 5, flines = filelines)

    # parameter = MaxRate
    filelines[289:(289 + 113)] = editted_lines(Ite = Ite, Num = 113, row_0 = 289, parameter = "MaxRate", Col = 1, flines = filelines)

    # parameter = MinRate
    filelines[289:(289 + 113)] = editted_lines(Ite = Ite, Num = 113, row_0 = 289, parameter = "MinRate", Col = 2, flines = filelines)

    # parameter = Decay
    filelines[289:(289 + 113)] = editted_lines(Ite = Ite, Num = 113, row_0 = 289, parameter = "Decay", Col = 3, flines = filelines)

    # parameter = DryTime
    filelines[289:(289 + 113)] = editted_lines(Ite = Ite, Num = 113, row_0 = 289, parameter = "DryTime", Col = 4, flines = filelines)
    # ---------------------------
    
    # ---------------------------
    # 1 = number of aquifers
    
    # parameter = Por
    filelines[406:(406 + 1)] = editted_lines(Ite = Ite, Num = 1, row_0 = 406, parameter = "Por", Col = 1, flines = filelines)

    # parameter = WP
    filelines[406:(406 + 1)] = editted_lines(Ite = Ite, Num = 1, row_0 = 406, parameter = "WP", Col = 2, flines = filelines)

    # parameter = FC
    filelines[406:(406 + 1)] = editted_lines(Ite = Ite, Num = 1, row_0 = 406, parameter = "FC", Col = 3, flines = filelines)

    # parameter = Ksat
    filelines[406:(406 + 1)] = editted_lines(Ite = Ite, Num = 1, row_0 = 406, parameter = "Ksat", Col = 4, flines = filelines)
    # ---------------------------
    
    # ---------------------------
    # 195 = number of conduits
    
    # # parameter = Rough
    # filelines[734:(734 + 195)] = editted_lines(Ite = Ite, Num = 195, row_0 = 734, parameter = "Rough", Col = 4, flines = filelines)
    # ---------------------------
    
    # ---------------------------
    # 1 = number of pollutants

    # parameter = Kdecay
    filelines[1125:(1125 + 1)] = editted_lines(Ite = Ite, Num = 1, row_0 = 1125, parameter = "Kdecay", Col = 5, flines = filelines)

    # parameter = BCoeff2
    filelines[1371:(1371 + 1)] = editted_lines(Ite = Ite, Num = 1, row_0 = 1371, parameter = "BCoeff2", Col = 4, flines = filelines)

    # parameter = WCoeff2
    filelines[1377:(1377 + 1)] = editted_lines(Ite = Ite, Num = 1, row_0 = 1377, parameter = "WCoeff2", Col = 4, flines = filelines)
    # ---------------------------
    

    # copy, write out file
    loginfo("Opening file <" + new_path + "> to overwrite with edited content.")
    new_file = open(new_path, "w")
    new_file.writelines(filelines)
    loginfo("Closing file <" + new_path + ">.")
    new_file.close()

# ----------------------------------------------
# the end
# ----------------------------------------------
