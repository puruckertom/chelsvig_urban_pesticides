# --------------------------------------------------
# run deterministic simulation
# --------------------------------------------------

# set up
from pyswmm import Simulation
import os

# specify location
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

file_path = dir_path + r'\input\swmm\NPlesantCreek.inp'
print(file_path)
print(os.path.exists(file_path))

binary_path = dir_path + r'\input\swmm\NPlesantCreek.out'

# load the model - no interaction, write out binary file
sim = Simulation(inputfile=file_path, reportfile=None, outputfile=binary_path)
sim.execute()










