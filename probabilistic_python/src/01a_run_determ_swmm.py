# --------------------------------------------------
# run deterministic simulation
# --------------------------------------------------

# set up
from pyswmm import Simulation
import os
from path_names import inp_path, bin_path

# delete pre-existing .out in order to run swmm
if os.path.exists(bin_path):
    print("Deleting current copy of <NPlesantCreek.out> so new copy can be created.")
    os.remove(bin_path)

# load the model - no interaction, write out binary file
sim = Simulation(inputfile=inp_path, reportfile=None, outputfile=bin_path)
sim.execute()










