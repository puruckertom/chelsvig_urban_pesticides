# ------------------------------------------------------------------------------------------
# execute vvwm for probabilistic simulations
# ------------------------------------------------------------------------------------------

# setup
import os, shutil, subprocess
from path_names import exe_path, vvwm_path, wet_path
from prpy_bookkeeping import *
loginfo = log_prefixer("09")

# number of simulations
try:
    nsims = main.nsims
except AttributeError:
    nsims = 5

# vvwm zones
outfalls = ['outfall_31_26', 'outfall_31_28', 'outfall_31_29', 'outfall_31_35',
            'outfall_31_36', 'outfall_31_38', 'outfall_31_42']

# loop through each outfall to create its vvwmTransfer.txt file
loginfo("Looping thru outfalls for navigating to each vwmm folder and then each of its " + str(nsims) + " input folders.")
for o in outfalls:

    # set pathways
    outfall_dir = os.path.join(vvwm_path, o)

    # run vvwm, for each sim
    loginfo("Looping thru simulations of " + o[1:] + " to create each simulation's vvwmTransfer.txt file.")
    for i in range(1, nsims + 1):
        sim_dir = os.path.join(outfall_dir, "input_" + str(i))

        # copy weather file into new file location
        old_wet_path = os.path.join(wet_path, "vvwm_wet.dvf")
        print(old_wet_path)
        new_wet_path = os.path.join(sim_dir, "vvwm_wet.dvf")
        print(new_wet_path)
        shutil.copyfile(old_wet_path, new_wet_path)

        # copy exe into new file location
        old_exe_path = os.path.join(exe_path, "VVWM.exe")
        new_exe_path = os.path.join(sim_dir, "VVWM.exe")
        shutil.copyfile(old_exe_path, new_exe_path)

        # copy vvwmTransfer.txt file into new location
        old_path = os.path.join(vvwm_path, "vvwmTransfer.txt")
        new_path = os.path.join(sim_dir, "vvwmTransfer.txt")
        shutil.copyfile(old_path, new_path)

        # read the new file, and update file pathways
        this_vvwm_file = open(new_path, 'r')
        filelines = this_vvwm_file.readlines()
        this_vvwm_file.close()

        filelines[0] = os.path.join(sim_dir, "output") + '\n'
        filelines[29] = os.path.join(sim_dir, "vvwm_wet.dvf") + '\n'
        filelines[68] = os.path.join(sim_dir, "output_NPlesant_Custom_parent_daily.csv") + '\n'
        filelines[69] = os.path.join(sim_dir, "output_NPlesant_Custom_deg1_daily.csv") + '\n'
        filelines[70] = os.path.join(sim_dir, "output_NPlesant_Custom_deg2_daily.csv") + '\n'
        filelines[71] = os.path.join(sim_dir, "output_NPlesant_Custom_parent_analysis.txt") + '\n'
        filelines[72] = os.path.join(sim_dir, "output_NPlesant_Custom_deg1_analysis.txt") + '\n'
        filelines[73] = os.path.join(sim_dir, "output_NPlesant_Custom_deg2_analysis.txt") + '\n'
        filelines[74] = os.path.join(sim_dir, "output_NPlesant_Custom_parent_deem.rdf") + '\n'
        filelines[75] = os.path.join(sim_dir, "output_NPlesant_Custom_deg1_deem.rdf") + '\n'
        filelines[76] = os.path.join(sim_dir, "output_NPlesant_Custom_deg2_deem.rdf") + '\n'
        filelines[77] = os.path.join(sim_dir, "output_NPlesant_Custom_parent_calendex.rdf") + '\n'
        filelines[78] = os.path.join(sim_dir, "output_NPlesant_Custom_deg1_calendex.rdf") + '\n'
        filelines[79] = os.path.join(sim_dir, "output_NPlesant_Custom_deg2_calendex.rdf") + '\n'
        filelines[80] = os.path.join(sim_dir, "output_NPlesant_Custom_parent_esa.txt") + '\n'
        filelines[81] = os.path.join(sim_dir, "output_NPlesant_Custom_deg1_esa.txt") + '\n'
        filelines[82] = os.path.join(sim_dir, "output_NPlesant_Custom_deg2_esa.txt") + '\n'

        # copy, write out file
        this_vvwm_file = open(new_path, 'w')
        this_vvwm_file.writelines(filelines)
        this_vvwm_file.close()

        # run vvwm.exe (vvwm.exe 'inputfilename')
        command = new_exe_path + ' ' + new_path
        print(command)
        subprocess.call(command)

