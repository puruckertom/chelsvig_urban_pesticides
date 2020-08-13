# --------------------------------------------------
# run deterministic simulation
# --------------------------------------------------

# set up
from pyswmm import Simulation
import os

# specify locations
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

# input file
file_path = dir_path + r'\input\swmm\NPlesantCreek.inp'
print(file_path)
print(os.path.exists(file_path))

# binary output file
binary_path = dir_path + r'\input\swmm\NPlesantCreek.out'

# delete pre-existing .out in order to run swmm
if os.path.exists(binary_path):
    os.remove(binary_path)
else:
    print("Can not delete the file as it doesn't exists")

# load the model - no interaction, write out binary file
sim = Simulation(inputfile=file_path, reportfile=None, outputfile=binary_path)
sim.execute()










