# --------------------------------------------------
# run [practice/dummy] simulation
# --------------------------------------------------

# set up
from pyswmm import Simulation, Subcatchments
import os, platform

# specify location
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

file_path = dir_path + r'\input\swmm\NPlesantCreek.inp'
print(file_path)
print(os.path.exists(file_path))

# load the model - no interaction
sim = Simulation(file_path)
for step in sim:
    pass
sim.report()










