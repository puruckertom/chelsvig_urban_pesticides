# ------------------------------------------------------------------------------------------
# examine the deterministic output
# ------------------------------------------------------------------------------------------

# setup
import pandas, os

# specify location
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

swmm_path = dir_path + r'\input\swmm'
print(swmm_path)
vvwm_path = dir_path + r'\input\vvwm'
print(vvwm_path)

outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42',]

for o in outfalls:
    # set pathways
    outfall_path = vvwm_path + o
    determ = outfall_path + r'\determ'
    vvwm_out = determ + r'\output_NPlesant_Custom_parent_daily.csv'
    swmm_out = determ + r'\output.zts'


    # read csv
    v_output = pandas.read_csv(vvwm_out, skiprows=[0, 6])
    # want the 2nd col (water col conc, kg/m3) and 3rd col (benthic zone conc, kg/m3)



    # read zts
    # skip over the first 3 lines
    # want the 6th column (mass of pesticide in runoff (g/ha/day)



# todo look at the outputs from vvwm run