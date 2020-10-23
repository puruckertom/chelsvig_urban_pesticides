# ------------------------------------------------------------------------------------------
# format outputs to be used later for plotting - probabilistic
# ------------------------------------------------------------------------------------------

# setup
import pandas as pd, os, numpy as np
from path_names import vvwm_path
import datetime as date

outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42']

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
for o in outfalls:
    # set pathways
    outfall_dir = vvwm_path + o
    for Ite in range(1, nsims + 1):
        input_dir = outfall_dir + r'\input_' + str(Ite)

        # swmm output time series file (vvwm input .zts)
        swmm_df = pd.read_table(input_dir + r'\output.zts', header=None, sep=",", skiprows=3, usecols = [3])
        array_swmm[:, :, Ite - 1] = swmm_df

        # vvwm output time series file (vvwm .csv)
        vvwm_df = pd.read_table(input_dir + r'\output_NPlesant_Custom_parent_daily.csv', header=None, sep=",",
                                    skiprows=5, usecols=[1,2]) * 1000000
        array_vvwm[:, :, Ite - 1] = vvwm_df

    # subset desired output variables (#shape = days*nsims)
    np.savetxt(outfall_dir + r'\prob_runf.txt', array_swmm[:, 0, :], delimiter=',')
    np.savetxt(outfall_dir + r'\prob_conc_h20.txt', array_vvwm[:, 0, :], delimiter=',')
    np.savetxt(outfall_dir + r'\prob_conc_benth.txt', array_vvwm[:, 1, :], delimiter=',')
