# --------------------------------------------------
# run probabilistic simulations, save output
# --------------------------------------------------

# setup
from pyswmm import Simulation
import os

# nsims
nsims = 5

# specify location
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

input_path = dir_path + r'\input\swmm\input_'
print(input_path)

# run swmm, for each sim
for i in range(1, nsims+1):
    sim_folder = input_path + str(i)
    sim_file = os.path.join(sim_folder, "NPlesantCreek.inp")

    binary_path = sim_folder + r'\NPlesantCreek.out'

    # delete pre-existing .out in order to run swmm
    if os.path.exists(binary_path):
        os.remove(binary_path)
    else:
        print("Can not delete the file as it doesn't exists")

    # load the model - no interaction, write out binary file
    sim = Simulation(inputfile=sim_file, reportfile=None, outputfile=binary_path)
    sim.execute()
