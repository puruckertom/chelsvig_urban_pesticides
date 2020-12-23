# --------------------------------------------------
# run deterministic simulation
# --------------------------------------------------

# set up
from pyswmm import Simulation
import os
from path_names import inp_path, bin_path
from prpy_bookkeeping import *
loginfo = log_prefixer("01a")

# delete pre-existing .out in order to run swmm
if os.path.exists(bin_path):
    loginfo("Deleting current copy of <" + bin_path + "> so new copy can be created.")
    print("Deleting current copy of <NPlesantCreek.out> so new copy can be created.")
    os.remove(bin_path)

replace_infile_abspaths(inp_path = inp_path, new_path = inp_path)

# load the model - no interaction, write out binary file
# Use loop to silence progress reports to conserve space and runtime
with Simulation(inputfile=inp_path, reportfile=None, outputfile=bin_path) as sim:
    loginfo("Executing SWMM simmulation with no interaction. Input from <" + inp_path + ">. Will store output in <" + bin_path + ">.")
    for step in sim:
        pass










