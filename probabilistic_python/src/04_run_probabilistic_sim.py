# --------------------------------------------------
# run probabilistic simulations, save output
# --------------------------------------------------

# todo run each of the probabilistic sim .inp files, and save the results to a cohesive data frame

# setup
from pyswmm import Simulation
import os

# nsims
nsims = 5

for i in range(1,nsims+1):
    simfolder = 'C:/Users/echelsvi/git/chelsvig_urban_pesticides/probabilistic_python/input/swmm/input_' + str(i)
    sim = Simulation('C:/Users/echelsvi/git/chelsvig_urban_pesticides/probabilistic_python/input/swmm/NPlesantCreek.inp')
