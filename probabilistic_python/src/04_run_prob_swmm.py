# --------------------------------------------------
# run probabilistic simulations, save output
# --------------------------------------------------

# setup
from pyswmm import Simulation
import os
from path_names import dir_path

# nsims
nsims = 5

# specify location
# print(os.path.abspath(os.curdir))
# os.chdir('..')
# dir_path = os.path.abspath(os.curdir)
# print(dir_path)

inp_dir_prefix = dir_path + r'\input\swmm\input_'
print(inp_dir_prefix)

# run swmm, for each sim
for i in range(1, nsims+1):
    sim_dir = inp_dir_prefix + str(i)
    sim_path = os.path.join(sim_dir, 'NPlesantCreek.inp')

    sim_bin_path = sim_dir + r'\NPlesantCreek.out'

    # delete pre-existing .out in order to run swmm
    if os.path.exists(sim_bin_path):
        print('Deleting current copy of <NPlesantCreek.out> so new copy can be created.')
        os.remove(sim_bin_path)

    # load the model - no interaction, write out binary file
    sim = Simulation(inputfile=sim_path, reportfile=None, outputfile=sim_bin_path)
    sim.execute()
