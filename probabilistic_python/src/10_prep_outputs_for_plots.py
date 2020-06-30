# ------------------------------------------------------------------------------------------
# merge the simulation outputs into a single data frame
# ------------------------------------------------------------------------------------------

# setup
import pandas, os, numpy as np

# specify location
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

vvwm_path = dir_path + r'\input\vvwm'
print(vvwm_path)

outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42',]

nsims = 5

# swmm output time series file (vvwm input .zts)
df_swmm = pandas.read_table(vvwm_path+r'\outfall_31_26\input_1\output.zts',
                            header=None, sep=",", skiprows=3)

# obtain structural dimensions
nrows_swmm = len(df_swmm)
print(nrows_swmm) #3287
ncols_swmm = len(df_swmm.columns)
print(ncols_swmm) #7

# create blank array with these dim
array_swmm = np.empty((nrows_swmm, ncols_swmm, nsims))
print(array_swmm.shape) #3287, 7, 5

# vvwm output time series file (vvwm .csv)
df_vvwm = pandas.read_table(vvwm_path+r'\outfall_31_26\input_1\output_NPlesant_Custom_parent_daily.csv',
                            header=None, sep=",", skiprows=5)
# obtain structural dimensions
nrows_vvwm = len(df_vvwm)
print(nrows_vvwm) #3287
ncols_vvwm = len(df_vvwm.columns)
print(ncols_vvwm) #4

# create blank array with these dim
array_vvwm = np.empty((nrows_vvwm, ncols_vvwm, nsims))
print(array_vvwm.shape) #3287, 4, 5

# loop
for o in outfalls:
    # set pathways
    outfall_path = vvwm_path + o
    for Ite in range(1, nsims + 1):
        folder = r'\input_' + str(Ite)
        input_folder = outfall_path + folder

        # swmm output time series file (vvwm input .zts)
        swmm_df = pandas.read_table(input_folder + r'\output.zts', header=None, sep=",", skiprows=3)
        array_swmm[0:nrows_swmm, 0:ncols_swmm, Ite - 1] = swmm_df

        # vvwm output time series file (vvwm .csv)
        vvwm_df = pandas.read_table(input_folder + r'\output_NPlesant_Custom_parent_daily.csv', header=None, sep=",",
                                    skiprows=5)
        array_vvwm[0:nrows_vvwm, 0:ncols_vvwm, Ite - 1] = vvwm_df

    # subset desired output variables (#shape = days*nsims)
    conc_runf = array_swmm[:, 3, :]
    np.savetxt(outfall_path + r'\conc_runf.txt', conc_runf, delimiter=',')

    conc_h20 = array_vvwm[:, 1, :] #bifenthrin concentration in water column (kg/m3)
    np.savetxt(outfall_path + r'\conc_h20.txt', conc_h20, delimiter=',')

    conc_benth = array_vvwm[:, 2, :] #bifenthrin concentration in benthic zone (kg/m3)
    np.savetxt(outfall_path + r'\conc_benth.txt', conc_benth, delimiter=',')


