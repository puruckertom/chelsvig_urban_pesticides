# ------------------------------------------------------------------------------------------
# format outputs to be used later for plotting - deterministic
# ------------------------------------------------------------------------------------------

# setup
import pandas as pd, os
from path_names import swmm_path, vvwm_path
from prpy_bookkeeping import *
loginfo = log_prefixer("01e")

outfalls = ['outfall_31_26', 'outfall_31_28', 'outfall_31_29', 'outfall_31_35',
            'outfall_31_36', 'outfall_31_38', 'outfall_31_42']

loginfo("Looping thru outfalls for navigating to each vwmm\determ folder where 3 files will be created/recreated.")
for o in outfalls:
    for o in outfalls:
        # set pathways
        outfall_dir = os.path.join(vvwm_path, o)
        determ_dir = os.path.join(outfall_dir, "determ")
        vvwm_out_path = os.path.join(determ_dir, "output_NPlesant_Custom_parent_daily.csv")
        swmm_out_path = os.path.join(determ_dir, "output.zts")

        # swmm output time series file (vvwm input .zts)
        loginfo("Reading in data from swmm output time series file <" + swmm_out_path + ">.")
        swmm_df = pd.read_table(swmm_out_path, header=None,
                                names=['year', 'month', 'day', 'runf_cmha', 'solids', 'runf_bif_gha', 'eros_bif_gha'],
                                sep=",", skiprows=3) 
        # 3 = daily water/field area that flows into water body (cm/ha/day)
        # 5 = mass of pesticide/field area entering water body by runoff (g/ha/day)
        swmm_df.loc[:, 'date'] = pd.Series(pd.date_range(start='1/1/2009', periods=len(swmm_df), freq='D'))

        # subset desired cols, write out
        runf = swmm_df.loc[:, ['runf_cmha', 'date']]
        loginfo("Writing to <" + outfall_dir + "\determ_runf.txt>.")
        runf.to_csv(os.path.join(outfall_dir, "determ_runf.txt"), index=False)

        # vvwm output time series file (vvwm .csv)
        loginfo("Reading in data from vvwm output time series file <" + vvwm_out_path + ">.")
        vvwm_df = pd.read_table(vvwm_out_path, header=None, names=['depth', 'conc_h20', 'conc_benth', 'conc_peak'], sep=",",
                                skiprows=5)
        # 1 = bifenthrin concentration in water column (kg/m3)
        # 2 = bifenthrin concentration in benthic zone (kg/m3)
        vvwm_df.loc[:, 'date'] = pd.Series(pd.date_range(start='1/1/2009', periods=len(vvwm_df), freq='D'))

        # subset desired cols, write out
        conc_h20 = vvwm_df.loc[:, ['conc_h20', 'date']]
        conc_h20['conc_h20'] = conc_h20['conc_h20'].apply(lambda x: x * 1000000)  # ug/L
        loginfo("Writing to <" + outfall_dir + "\determ_conc_h20.txt>.")
        conc_h20.to_csv(os.path.join(outfall_dir, "determ_conc_h20.txt"), index=False)

        conc_benth = vvwm_df.loc[:, ['conc_benth', 'date']]
        conc_benth['conc_benth'] = conc_benth['conc_benth'].apply(lambda x: x * 1000000)  # ug/L
        loginfo("Writing to <" + outfall_dir + "\determ_conc_benth.txt>.")
        conc_benth.to_csv(os.path.join(outfall_dir, "determ_conc_benth.txt"), index=False)



