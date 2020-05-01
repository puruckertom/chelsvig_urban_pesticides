# --------------------------------------------------
# run probabilistic simulations, save output
# --------------------------------------------------

# todo run each of the probabilistic sim .inp files, and save the results to a cohesive data frame

# setup
from pyswmm import Simulation
import os, pandas
# specify location
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

input_path = dir_path + r'\input\swmm\input_'
print(input_path)

# nsims
nsims = 5



# run swmm, for each sim
for i in range(1, nsims+1):
    sim_folder = input_path + str(i)
    sim_file = os.path.join(sim_folder, "NPlesantCreek.inp")

    sim = Simulation(sim_file)
    for step in sim:
        pass
    sim.report()


# todo set up dataframe to receive the outputs from the simulations
# todo grab the desired output variable of interest, and store in dataframe

