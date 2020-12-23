# ------------------------------------------------------------------------------------------
# execute vvwm for deterministic simulation
# ------------------------------------------------------------------------------------------

# setup
import os, shutil, subprocess, re
from path_names import exe_path, vvwm_path, wet_path
from prpy_bookkeeping import *
loginfo = log_prefixer("01d")

outfalls = ['outfall_31_26', 'outfall_31_28', 'outfall_31_29', 'outfall_31_35',
            'outfall_31_36', 'outfall_31_38', 'outfall_31_42']

loginfo("Looping thru outfalls for navigating to each vwmm folder where its .zts file will be created.")
for o in outfalls:
    # set pathways
    outfall_dir = os.path.join(vvwm_path, o)
    determ_dir = os.path.join(outfall_dir, "determ")

    # copy weather file into new file location
    old_wet_path = os.path.join(wet_path, "vvwm_wet.dvf")
    print(old_wet_path)
    new_wet_path = os.path.join(determ_dir, "vvwm_wet.dvf")
    print(new_wet_path)
    loginfo("Copying weather, exe, and vvwmTransfer files into" + o[1:] + " determ folder.")
    shutil.copyfile(old_wet_path, new_wet_path)

    # copy exe into new file location
    old_exe_path = os.path.join(exe_path, "VVWM.exe")
    new_exe_path = os.path.join(determ_dir, "VVWM.exe")
    shutil.copyfile(old_exe_path, new_exe_path)

    # copy vvwmTransfer.txt file into new location
    old_path = os.path.join(vvwm_path, "vvwmTransfer.txt")
    new_path = os.path.join(determ_dir, "vvwmTransfer.txt")
    shutil.copyfile(old_path, new_path)

    # read the new file, and update file pathways
    loginfo("Opening file <" + new_path + "> to read content out of.")
    this_vvwm_file = open(new_path, 'r')
    filelines = this_vvwm_file.readlines()
    loginfo("Closing file <" + new_path + ">.")
    this_vvwm_file.close()

    filelines[0] = os.path.join(determ_dir, "output") + '\n'
    filelines[29] = os.path.join(determ_dir, "vvwm_wet.dvf") + '\n'
    filelines[68] = os.path.join(determ_dir, "output_NPlesant_Custom_parent_daily.csv") + '\n'
    filelines[69] = os.path.join(determ_dir, "output_NPlesant_Custom_deg1_daily.csv") + '\n'
    filelines[70] = os.path.join(determ_dir, "output_NPlesant_Custom_deg2_daily.csv") + '\n'
    filelines[71] = os.path.join(determ_dir, "output_NPlesant_Custom_parent_analysis.txt") + '\n'
    filelines[72] = os.path.join(determ_dir, "output_NPlesant_Custom_deg1_analysis.txt") + '\n'
    filelines[73] = os.path.join(determ_dir, "output_NPlesant_Custom_deg2_analysis.txt") + '\n'
    filelines[74] = os.path.join(determ_dir, "output_NPlesant_Custom_parent_deem.rdf") + '\n'
    filelines[75] = os.path.join(determ_dir, "output_NPlesant_Custom_deg1_deem.rdf") + '\n'
    filelines[76] = os.path.join(determ_dir, "output_NPlesant_Custom_deg2_deem.rdf") + '\n'
    filelines[77] = os.path.join(determ_dir, "output_NPlesant_Custom_parent_calendex.rdf") + '\n'
    filelines[78] = os.path.join(determ_dir, "output_NPlesant_Custom_deg1_calendex.rdf") + '\n'
    filelines[79] = os.path.join(determ_dir, "output_NPlesant_Custom_deg2_calendex.rdf") + '\n'
    filelines[80] = os.path.join(determ_dir, "output_NPlesant_Custom_parent_esa.txt") + '\n'
    filelines[81] = os.path.join(determ_dir, "output_NPlesant_Custom_deg1_esa.txt") + '\n'
    filelines[82] = os.path.join(determ_dir, "output_NPlesant_Custom_deg2_esa.txt") + '\n'

    # copy, write out file
    loginfo("Opening file <" + new_path + "> to overwrite with edited content.")
    this_vvwm_file = open(new_path, 'w')
    this_vvwm_file.writelines(filelines)
    loginfo("Closing file <" + new_path + ">.")
    this_vvwm_file.close()

    # todo get the executable to work with python code
    # run vvwm.exe (vvwm.exe 'inputfilename')
    logging.info("01d. Running <vvwm.exe> on <" + new_path + ">.")
    subprocess.call([new_exe_path, new_path])
    
