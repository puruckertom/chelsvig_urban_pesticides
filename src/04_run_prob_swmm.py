# --------------------------------------------------
# run probabilistic simulations, save output
# --------------------------------------------------

# setup
from pyswmm import Simulation
import swmmtoolbox.swmmtoolbox as swmmtoolbox
import os, dask, shutil, time, pandas as pd
from path_names import dir_path
from pyswmm.lib import DLL_SELECTION
from prpy_bookkeeping import *
loginfo = log_prefixer("04")

# number of simulations
try:
    nsims = main.nsims
except AttributeError:
    nsims = 5

inp_dir_prefix = os.path.join(dir_path, "input", "swmm", "input_")
print(inp_dir_prefix)
# save the path for the original dynamic link library
dll_path = DLL_SELECTION()
# save its base name (just the name of the file)
dll_bn = os.path.basename(dll_path)
# save the path to a new folder where copies of dll will be stored upon creation
dll_dir = os.path.join(dir_path, "input", "swmm", "dll")
# make sure that folder exists. If it doesn't, create it.
if not os.path.exists(dll_dir):
    loginfo("Creating directory <" + dll_dir + ">.")
    print("Creating <dll/> directory.")
    os.mkdir(dll_dir)

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
    # create path to the 1-time-use dll file we are going to create
    dll_i = dll_bn[:dll_bn.rindex(".")] + '-' + str(i) + dll_bn[dll_bn.rindex("."):]
    lib_path = os.path.join(dll_dir, dll_i)
    # create 1-time-use dll file copy
    shutil.copyfile(dll_path, lib_path)
    # specify the directory with the file pyswmm needs by attaching the folder id to the rest of the folder's absolute path
    sim_dir = inp_dir_prefix + str(i)
    # specify the actual file pyswmm needs
    sim_path = os.path.join(sim_dir, r'NPlesantCreek.inp')
    #print("Simulation input file found:", sim_path)
    # specify the file that pyswmm will (over)write with output after running the probabilistic simulation
    sim_bin_path = os.path.join(sim_dir, "NPlesantCreek.out")
    # delete pre-existing .out, if present, in order to run swmm agreeably
    if os.path.exists(sim_bin_path):
        loginfo("Deleting current copy of <" + sim_bin_path + "> so new copy can be created.")
        #print("Deleting current copy of <NPlesantCreek.out> so new copy can be created.")
        os.remove(sim_bin_path)
    # stagger starting times 1 sec apart
    time.sleep(i)
    # load the model {no interaction, write (binary) results to <JS_NPlesantCreek.out>, use the specified dll}
    sim = Simulation(inputfile=sim_path, reportfile=None, outputfile=sim_bin_path, swmm_lib_path=lib_path)
    # simulate the loaded model
    loginfo("Executing SWMM simmulation with no interaction. Input from <" + sim_path + ">. Will store output in <" + sim_bin_path + ">.")
    # sim.execute()
    with sim as s:
        for step in s:
            pass

    # extract swmm outputs with swmmtoolbox and delete expensive binary files
    lab1 = 'subcatchment,,Runoff_rate'
    lab2 = 'subcatchment,,Bifenthrin'
    runf_stack = swmmtoolbox.extract(sim_bin_path, lab1)
    bif_stack = swmmtoolbox.extract(sim_bin_path, lab2)

    loginfo("Deleting <" + sim_bin_path + "> to free up memory.")
    os.remove(sim_bin_path)
    loginfo("Deleting <" + dll_i + "> to free up memory.")
    os.system("rm " + lib_path)
    print("Deleted <input_" + str(i) + "/JS_NPlesantCreek.out> and <" + dll_i + "> to free up memory.")    

    # compute and export daily averages to csv files and finish
    runf_davg = runf_stack.resample('D').mean()
    bif_davg = bif_stack.resample('D').mean()
    print(save_and_finish(runf_davg, os.path.join(sim_dir, "swmm_output_davg_runf.csv")))
    print(save_and_finish(bif_davg, os.path.join(sim_dir, "swmm_output_davg_bif.csv")))
    # msg1 and msg2 text will be the same, but we must do both to save both csvs
    
    # a message to indicate success
    return("file " + str(i) + " simulated!")

# set up the processes for each of the 5 simulations
delayed_tasks = [delay_job(x) for x in range(1, nsims+1)]

# hit go!
dask.delayed(print)(delayed_tasks).compute()
