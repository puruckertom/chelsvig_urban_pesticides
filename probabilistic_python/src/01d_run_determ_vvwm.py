# ------------------------------------------------------------------------------------------
# execute vvwm for deterministic simulation
# ------------------------------------------------------------------------------------------

# setup
import pandas, os, shutil, subprocess
from subprocess import Popen, PIPE

# specify location
print(os.path.abspath(os.curdir))
os.chdir("..")
dir_path = os.path.abspath(os.curdir)
print(dir_path)

swmm_path = dir_path + r'\input\swmm'
swmm_file = swmm_path + r'\NPlesantCreek.rpt'
inp_file = swmm_path + r'\NPlesantCreek.inp'
vvwm_path = dir_path + r'\input\vvwm'
exe_path = dir_path + r'\exe'
wet_path = dir_path + r'\weather'

outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42',]

for o in outfalls:
    # set pathways
    outfall_path = vvwm_path + o
    determ = outfall_path + r'\determ'

    # copy weather file into new file location
    old_wet = wet_path + r'\vvwm_wet.dvf'
    print(old_wet)
    new_wet = determ + r'\vvwm_wet.dvf'
    print(new_wet)
    shutil.copyfile(old_wet, new_wet)

    # copy exe into new file location
    old_exe = os.path.join(exe_path, "VVWM.exe")
    new_exe = os.path.join(determ, "VVWM.exe")
    shutil.copyfile(old_exe, new_exe)

    # copy vvwmTransfer.txt file into new location
    old_file = os.path.join(vvwm_path, "vvwmTransfer.txt")
    new_file = os.path.join(determ, "vvwmTransfer.txt")
    shutil.copyfile(old_file, new_file)

    # read the new file, and update file pathways
    this_vvwm = open(new_file, "r")
    filelines = this_vvwm.readlines()

    filelines[0] = determ + r'\output' + "\n"
    # pathway for respective weather file
    filelines[29] = determ + r'\vvwm_wet.dvf' + "\n"
    filelines[68] = determ + r'\output_NPlesant_Custom_parent_daily.csv' + "\n"
    filelines[69] = determ + r'\output_NPlesant_Custom_deg1_daily.csv' + "\n"
    filelines[70] = determ + r'\output_NPlesant_Custom_deg2_daily.csv' + "\n"
    filelines[71] = determ + r'\output_NPlesant_Custom_parent_analysis.txt' + "\n"
    filelines[72] = determ + r'\output_NPlesant_Custom_deg1_analysis.txt' + "\n"
    filelines[73] = determ + r'\output_NPlesant_Custom_deg2_analysis.txt' + "\n"
    filelines[74] = determ + r'\output_NPlesant_Custom_parent_deem.rdf' + "\n"
    filelines[75] = determ + r'\output_NPlesant_Custom_deg1_deem.rdf' + "\n"
    filelines[76] = determ + r'\output_NPlesant_Custom_deg2_deem.rdf' + "\n"
    filelines[77] = determ + r'\output_NPlesant_Custom_parent_calendex.rdf' + "\n"
    filelines[78] = determ + r'\output_NPlesant_Custom_deg1_calendex.rdf' + "\n"
    filelines[79] = determ + r'\output_NPlesant_Custom_deg2_calendex.rdf' + "\n"
    filelines[80] = determ + r'\output_NPlesant_Custom_parent_esa.txt' + "\n"
    filelines[81] = determ + r'\output_NPlesant_Custom_deg1_esa.txt' + "\n"
    filelines[82] = determ + r'\output_NPlesant_Custom_deg2_esa.txt' + "\n"

    # copy, write out file
    this_vvwm = open(new_file, "w")
    this_vvwm.writelines(filelines)
    this_vvwm.close()

    # todo get the executable to work with python code
    # run vvwm.exe (vvwm.exe "inputfilename")
    command = new_exe + " " + new_file
    print(command)
    subprocess.call(command)
