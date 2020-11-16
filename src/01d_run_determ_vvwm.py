# ------------------------------------------------------------------------------------------
# execute vvwm for deterministic simulation
# ------------------------------------------------------------------------------------------

# setup
import os, shutil, subprocess, re
from path_names import exe_path, vvwm_path, wet_path
from prpy_bookkeeping import *

outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42']

loginfo("Looping thru outfalls for navigating to each vwmm folder where its .zts file will be created.")
for o in outfalls:
    # set pathways
    outfall_dir = vvwm_path + o
    determ_dir = outfall_dir + r'\determ'

    # copy weather file into new file location
    old_wet_path = wet_path + r'\vvwm_wet.dvf'
    print(old_wet_path)
    new_wet_path = determ_dir + r'\vvwm_wet.dvf'
    print(new_wet_path)
    loginfo("Copying weather, exe, and vvwmTransfer files into" + o[1:] + " determ folder.")
    shutil.copyfile(old_wet_path, new_wet_path)

    # copy exe into new file location
    old_exe_path = exe_path + r'\VVWM.exe'
    new_exe_path = determ_dir + r'\VVWM.exe'
    shutil.copyfile(old_exe_path, new_exe_path)

    # copy vvwmTransfer.txt file into new location
    old_path = vvwm_path + r'\vvwmTransfer.txt'
    new_path = determ_dir + r'\vvwmTransfer.txt'
    shutil.copyfile(old_path, new_path)

    # read the new file, and update file pathways
    loginfo("Opening file <" + new_path + "> to read content out of.")
    this_vvwm_file = open(new_path, 'r')
    filelines = this_vvwm_file.readlines()
    loginfo("Closing file <" + new_path + ">.")
    this_vvwm_file.close()

    filelines[0] = determ_dir + r'\output' + '\n'
    # pathway for respective weather file
    filelines[29] = determ_dir + r'\vvwm_wet.dvf' + '\n'
    filelines[68] = determ_dir + r'\output_NPlesant_Custom_parent_daily.csv' + '\n'
    filelines[69] = determ_dir + r'\output_NPlesant_Custom_deg1_daily.csv' + '\n'
    filelines[70] = determ_dir + r'\output_NPlesant_Custom_deg2_daily.csv' + '\n'
    filelines[71] = determ_dir + r'\output_NPlesant_Custom_parent_analysis.txt' + '\n'
    filelines[72] = determ_dir + r'\output_NPlesant_Custom_deg1_analysis.txt' + '\n'
    filelines[73] = determ_dir + r'\output_NPlesant_Custom_deg2_analysis.txt' + '\n'
    filelines[74] = determ_dir + r'\output_NPlesant_Custom_parent_deem.rdf' + '\n'
    filelines[75] = determ_dir + r'\output_NPlesant_Custom_deg1_deem.rdf' + '\n'
    filelines[76] = determ_dir + r'\output_NPlesant_Custom_deg2_deem.rdf' + '\n'
    filelines[77] = determ_dir + r'\output_NPlesant_Custom_parent_calendex.rdf' + '\n'
    filelines[78] = determ_dir + r'\output_NPlesant_Custom_deg1_calendex.rdf' + '\n'
    filelines[79] = determ_dir + r'\output_NPlesant_Custom_deg2_calendex.rdf' + '\n'
    filelines[80] = determ_dir + r'\output_NPlesant_Custom_parent_esa.txt' + '\n'
    filelines[81] = determ_dir + r'\output_NPlesant_Custom_deg1_esa.txt' + '\n'
    filelines[82] = determ_dir + r'\output_NPlesant_Custom_deg2_esa.txt' + '\n'

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
    
