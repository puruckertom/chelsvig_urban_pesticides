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

# todo look at the outputs from vvwm run
