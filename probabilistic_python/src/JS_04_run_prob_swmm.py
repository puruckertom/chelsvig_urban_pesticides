# --------------------------------------------------
# run probabilistic simulations, save output
# --------------------------------------------------

# setup
from pyswmm import Simulation
import os
from path_names import dir_path

# nsims
nsims = 2

# specify location
# print(os.path.abspath(os.curdir))
# os.chdir("..")
# dir_path = os.path.abspath(os.curdir)
# print(dir_path)

inp_dir_prefix = dir_path + r'\input\swmm\input_'
print(inp_dir_prefix)

# run swmm, for each sim
for i in range(1, nsims+1):
    sim_folder = inp_dir_prefix + str(i)
    sim_file = os.path.join(sim_folder, "JS_NPlesantCreek.inp")

    sim_bin = sim_folder + r'\JS_NPlesantCreek.out'

    # delete pre-existing .out in order to run swmm
    if os.path.exists(sim_bin):
        print("Deleting current copy of <JS_NPlesantCreek.out> so new copy can be created.")
        os.remove(sim_bin)

    # load the model - no interaction, write out binary file
    sim = Simulation(inputfile=sim_file, reportfile=None, outputfile=sim_bin)
    sim.execute()
