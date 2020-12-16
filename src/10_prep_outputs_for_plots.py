# ------------------------------------------------------------------------------------------
# format outputs to be used later for plotting - probabilistic
# ------------------------------------------------------------------------------------------

# setup
import pandas as pd, os, numpy as np
from path_names import vvwm_path
import datetime as date
from prpy_bookkeeping import *
loginfo = log_prefixer("10")

# outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
#             '\outfall_31_36', '\outfall_31_38', '\outfall_31_42']
outfalls = ['outfall_31_26', 'outfall_31_28', 'outfall_31_29', 'outfall_31_35',
            'outfall_31_36', 'outfall_31_38', 'outfall_31_42']

# number of simulations
try:
    nsims = main.nsims
except AttributeError:
    nsims = 5

# SWMM output: obtain structural dimensions
ndays = (date.date(2018,1,1) - date.date(2009,1,1)).days
print(ndays) #3287
# create blank array with appropriate dim
array_swmm = np.zeros((ndays, 1, nsims))
print(array_swmm.shape) #3287, 5

# VVWM output: create blank array with appropriate dim
array_vvwm = np.zeros((ndays, 2, nsims))
print(array_vvwm.shape) #3287, 2, 5

# loop
loginfo("Looping thru outfalls for navigating to each vwmm folder and then each of its " + str(nsims) + " input folders.")
for o in outfalls:
    # set pathways
    outfall_dir = os.path.join(vvwm_path, o)#vvwm_path + o
    loginfo("Looping thru simulations of " + o[1:] + " to extract certain parts of each simulation's vvwm output file data.")
    for Ite in range(1, nsims + 1):
        input_dir = os.path.join(outfall_dir, "input_" + str(Ite))#outfall_dir + r'\input_' + str(Ite)

        # swmm output time series file (vvwm input .zts)
        swmm_df = pd.read_table(os.path.join(input_dir, "output.zts"), header=None, sep=",", skiprows=3, usecols = [3])#input_dir + r'\output.zts', header=None, sep=",", skiprows=3, usecols = [3])
        array_swmm[:, :, Ite - 1] = swmm_df

        # vvwm output time series file (vvwm .csv)
        vvwm_df = pd.read_table(os.path.join(input_dir, "output_NPlesant_Custom_parent_daily.csv"), header=None, sep=",",#input_dir + r'\output_NPlesant_Custom_parent_daily.csv', header=None, sep=",",
                                    skiprows=5, usecols=[1,2]) * 1000000
        array_vvwm[:, :, Ite - 1] = vvwm_df

    # subset desired output variables (#shape = days*nsims)
    loginfo("Making prob_runf.txt, prob_conc_h20.txt, and prob_conc_benth.txt with the data from all " + o[1:] + "'s simulations.")
    np.savetxt(os.path.join(outfall_dir, "prob_runf.txt"), array_swmm[:, 0, :], delimiter=',')#outfall_dir + r'\prob_runf.txt', array_swmm[:, 0, :], delimiter=',')
    np.savetxt(os.path.join(outfall_dir, "prob_conc_h20.txt"), array_vvwm[:, 0, :], delimiter=',')#outfall_dir + r'\prob_conc_h20.txt', array_vvwm[:, 0, :], delimiter=',')
    np.savetxt(os.path.join(outfall_dir, "prob_conc_benth.txt"), array_vvwm[:, 1, :], delimiter=',')#outfall_dir + r'\prob_conc_benth.txt', array_vvwm[:, 1, :], delimiter=',')
