# ------------------------------------------------------------------------------------------
# create .zts file for vvwm (for probabilistic sims)
# ------------------------------------------------------------------------------------------

# setup
import pandas, os
from datetime import date

# specify location
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

input_path = dir_path + r'\input\swmm\input_'
print(input_path)

#todo for each simulation, create a .zts file using the .csv files created in 05_ (use code from 01c_)