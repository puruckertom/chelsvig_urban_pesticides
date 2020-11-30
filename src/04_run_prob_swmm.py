# --------------------------------------------------
# run probabilistic simulations, save output
# --------------------------------------------------

# setup
from pyswmm import Simulation
import os, dask, shutil, time
from path_names import dir_path
from pyswmm.lib import DLL_SELECTION
from prpy_bookkeeping import *

# nsims
nsims = 5

inp_dir_prefix = os.path.join(dir_path, "input", "swmm", "input_")#dir_path + r'\input\swmm\input_'
print(inp_dir_prefix)
# save the path for the original dynamic link library
dll_path = DLL_SELECTION()
print(dll_path)

'''
Makes arrangements for executing the following task:
    Run specified probabilistic simulations in SWMM from the specified .inp file. Save output in equivalently named .out file.
Inputs:
    i <integer> -indicates input folder id number (for now, will only ever be 1-5).-
Immediate Output:
    <dask.delayed.Delayed> -arrangements for executing the task when commanded at a future time (by the 'compute()' function)
Computable Output:
    <string> -message indicating that the simulation has been completed on the .inp file in the 'i' input folder.-
'''

# this decorator is the first step in using dask to parallelize swmm simulations
@dask.delayed
def delay_job(i):
    loginfo("Simmulation " + str(i) + " of " + str(nsims))
    # create path to the .exe we are going to create
    lib_path = dll_path[:dll_path.rindex(".")] + '-' + str(i) + dll_path[dll_path.rindex("."):] #dll_path[-4:]#[:-4]+'-'+str(i)+dll_path[-4:]
    # create .exe file
    shutil.copyfile(dll_path, lib_path)
    # specify the directory with the file pyswmm needs by attaching the folder id to the rest of the folder's absolute path
    sim_folder = inp_dir_prefix + str(i)
    # specify the actual file pyswmm needs
    sim_file = os.path.join(sim_folder, r'NPlesantCreek.inp')
    print("Simulation input file found:", sim_file)
    # specify the file that pyswmm will (over)write with output after running the probabilistic simulation
    binary_file = os.path.join(sim_folder, "NPlesantCreek.out")#sim_folder + r'\NPlesantCreek.out'
    # delete pre-existing .out, if present, in order to run swmm agreeably
    if os.path.exists(binary_file):
        loginfo("Deleting current copy of <" + binary_file + "> so new copy can be created.")
        print("Deleting current copy of <NPlesantCreek.out> so new copy can be created.")
        os.remove(binary_file)
    # stagger starting times 1 sec apart
    time.sleep(i)
    # load the model {no interaction, write (binary) results to <JS_NPlesantCreek.out>, use the specified dll}
    sim = Simulation(inputfile=sim_file, reportfile=None, outputfile=binary_file, swmm_lib_path=lib_path)
    # simulate the loaded model
    loginfo("Executing SWMM simmulation with no interaction. Input from <" + sim_file + ">. Will store output in <" + binary_file + ">.")
    sim.execute()
    # a message to indicate success
    return("file " + str(i) + " simulated!")

# set up the processes for each of the 5 simulations
delayed_tasks = [delay_job(x) for x in range(1, nsims+1)]

# hit go!
dask.delayed(print)(delayed_tasks).compute()
