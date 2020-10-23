# ------------------------------------------------------------------------------------------
# format outputs to be used later for plotting - probabilistic
# ------------------------------------------------------------------------------------------

# setup
import pandas as pd, os, numpy as np
from path_names import vvwm_path
import datetime as date

# specify location
# print(os.path.abspath(os.curdir))
# os.chdir("..")
# dir_path = os.path.abspath(os.curdir)
# print(dir_path)

# vvwm_path = dir_path + r'\input\vvwm'
# print(vvwm_path)

outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42']

nsims = 5

# swmm output time series file (vvwm input .zts)
# df_swmm = pd.read_table(vvwm_path+r'\outfall_31_26\input_1\output.zts', header=None, sep=",", skiprows=3) 

# obtain structural dimensions
# ndays = len(df_swmm)
ndays = (date.date(2018,1,1) - date.date(2009,1,1)).days
print(ndays) #3287
# ncols_swmm = len(df_swmm.columns)
# print(ncols_swmm) #7

# create blank array with these dim
#array_swmm = np.empty((ndays, ncols_swmm, nsims))
array_swmm = np.zeros((ndays, 1, nsims))
print(array_swmm.shape) #3287, 5

# vvwm output time series file (vvwm .csv)
# df_vvwm = pd.read_table(vvwm_path+r'\outfall_31_26\input_1\output_NPlesant_Custom_parent_daily.csv',
#                         header=None, sep=",", skiprows=5)
# obtain structural dimensions
# ndays = len(df_vvwm)

# ncols_vvwm = len(df_vvwm.columns)
# print(ncols_vvwm) #4

# create blank array with these dim
#array_vvwm = np.empty((ndays, ncols_vvwm, nsims))
array_vvwm = np.zeros((ndays, 2, nsims))
print(array_vvwm.shape) #3287, 2, 5

# loop
for o in outfalls:
    # set pathways
    outfall_dir = vvwm_path + o
    for Ite in range(1, nsims + 1):
        input_dir = outfall_dir + r'\input_' + str(Ite)

        # # swmm output time series file (vvwm input .zts)
        # swmm_df = pd.read_table(input_dir + r'\output.zts', header=None, sep=",", skiprows=3,
        #                         names=['year', 'month', 'day', 'runf_cmha', 'solids', 'runf_bif_gha', 'eros_bif_gha'])
        # #array_swmm[0:ndays, 0:ncols_swmm, Ite - 1] = swmm_df
        # array_swmm[:, :, Ite - 1] = swmm_df
        
        swmm_df = pd.read_table(input_dir + r'\output.zts', header=None, sep=",", skiprows=3, usecols = [3])
        #array_swmm[0:ndays, 0:ncols_swmm, Ite - 1] = swmm_df
        array_swmm[:, :, Ite - 1] = swmm_df

        # vvwm output time series file (vvwm .csv)
        # vvwm_df = pd.read_table(input_dir + r'\output_NPlesant_Custom_parent_daily.csv', header=None, sep=",",
        #                             skiprows=5, names=['depth', 'conc_h20', 'conc_benth', 'conc_peak'])
        vvwm_df = pd.read_table(input_dir + r'\output_NPlesant_Custom_parent_daily.csv', header=None, sep=",",
                                    skiprows=5, usecols=[1,2]) * 1000000
        #array_vvwm[0:ndays, 0:ncols_vvwm, Ite - 1] = vvwm_df
        array_vvwm[:, :, Ite - 1] = vvwm_df

    # subset desired output variables (#shape = days*nsims)
    # conc_runf = array_swmm[:, 3, :]
    # np.savetxt(outfall_dir + r'\prob_runf.txt', conc_runf, delimiter=',')
    np.savetxt(outfall_dir + r'\prob_runf.txt', array_swmm[:, 0, :], delimiter=',')


    # conc_h20 = array_vvwm[:, 1, :]  # bifenthrin concentration in water column kg/m3
    # conc_h20 = conc_h20 * 1000000  # ug/L
    np.savetxt(outfall_dir + r'\prob_conc_h20.txt', array_vvwm[:, 0, :], delimiter=',')

    # conc_benth = array_vvwm[:, 2, :]  # bifenthrin concentration in benthic zone kg/m3
    # conc_benth = conc_benth * 1000000  # ug/L
    np.savetxt(outfall_dir + r'\prob_conc_benth.txt', array_vvwm[:, 1, :], delimiter=',')
