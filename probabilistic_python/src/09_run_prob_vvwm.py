# ------------------------------------------------------------------------------------------
# execute vvwm for probabilistic simulations
# ------------------------------------------------------------------------------------------

# setup
import pandas, os, shutil, subprocess

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
wet_path = dir_path + r'\weather\vvwm'

# nsims
nsims = 5

# vvwm zones
outfalls = ['\outfall_31_26', '\outfall_31_28', '\outfall_31_29', '\outfall_31_35',
            '\outfall_31_36', '\outfall_31_38', '\outfall_31_42',]

# loop through each outfall to create its vvwm.zts input file
for o in outfalls:

    # set pathways
    outfall_path = vvwm_path + o

    # run vvwm, for each sim
    for i in range(1, nsims + 1):
        sim_folder = outfall_path + r"\input_" + str(i)

        # assign weather files to respective outfalls
        if o == '\outfall_31_26' or o == '\outfall_31_28' or o == '\outfall_31_29' or o == '\outfall_31_42':
            # copy weather file into new file location
            old_wet = wet_path + r'\weather_STA01.dvf'
            print(old_wet)
            new_wet = sim_folder + r'\weather_STA01.dvf'
            print(new_wet)
            shutil.copyfile(old_wet, new_wet)

        elif o == '\outfall_31_36':
            # copy weather file into new file location
            old_wet = wet_path + r'\weather_p1572.dvf'
            print(old_wet)
            new_wet = sim_folder + r'\weather_p1572.dvf'
            print(new_wet)
            shutil.copyfile(old_wet, new_wet)

        elif o == '\outfall_31_35':
            old_wet = wet_path + r'\weather_P1601.dvf'
            print(old_wet)
            new_wet = sim_folder + r'\weather_P1601.dvf'
            print(new_wet)
            shutil.copyfile(old_wet, new_wet)

        elif o == '\outfall_31_38':
            old_wet = wet_path + r'\weather_P1602.dvf'
            print(old_wet)
            new_wet = sim_folder + r'\weather_P1602.dvf'
            print(new_wet)
            shutil.copyfile(old_wet, new_wet)

        # copy exe into new file location
        old_exe = exe_path + r"\VVWM.exe"
        new_exe = sim_folder + r"\VVWM.exe"
        shutil.copyfile(old_exe, new_exe)

        # copy vvwmTransfer.txt file into new location
        old_file = vvwm_path + r"\vvwmTransfer.txt"
        new_file = sim_folder + r"\vvwmTransfer.txt"
        shutil.copyfile(old_file, new_file)

        # read the new file, and update file pathways
        this_vvwm = open(new_file, "r")
        filelines = this_vvwm.readlines()

        filelines[0] = sim_folder + r'\output' + "\n"

        # pathway for respective weather file
        if o == '\outfall_31_26' or o == '\outfall_31_28' or o == '\outfall_31_29' or o == '\outfall_31_42':
            filelines[29] = sim_folder + r'\weather_STA01.dvf' + "\n"
        elif o == '\outfall_31_36':
            filelines[29] = sim_folder + r'\weather_p1572.dvf' + "\n"
        elif o == '\outfall_31_35':
            filelines[29] = sim_folder + r'\weather_P1601.dvf' + "\n"
        elif o == '\outfall_31_38':
            filelines[29] = sim_folder + r'\weather_P1602.dvf' + "\n"
        filelines[68] = sim_folder + r'\output_NPlesant_Custom_parent_daily.csv' + "\n"
        filelines[69] = sim_folder + r'\output_NPlesant_Custom_deg1_daily.csv' + "\n"
        filelines[70] = sim_folder + r'\output_NPlesant_Custom_deg2_daily.csv' + "\n"
        filelines[71] = sim_folder + r'\output_NPlesant_Custom_parent_analysis.txt' + "\n"
        filelines[72] = sim_folder + r'\output_NPlesant_Custom_deg1_analysis.txt' + "\n"
        filelines[73] = sim_folder + r'\output_NPlesant_Custom_deg2_analysis.txt' + "\n"
        filelines[74] = sim_folder + r'\output_NPlesant_Custom_parent_deem.rdf' + "\n"
        filelines[75] = sim_folder + r'\output_NPlesant_Custom_deg1_deem.rdf' + "\n"
        filelines[76] = sim_folder + r'\output_NPlesant_Custom_deg2_deem.rdf' + "\n"
        filelines[77] = sim_folder + r'\output_NPlesant_Custom_parent_calendex.rdf' + "\n"
        filelines[78] = sim_folder + r'\output_NPlesant_Custom_deg1_calendex.rdf' + "\n"
        filelines[79] = sim_folder + r'\output_NPlesant_Custom_deg2_calendex.rdf' + "\n"
        filelines[80] = sim_folder + r'\output_NPlesant_Custom_parent_esa.txt' + "\n"
        filelines[81] = sim_folder + r'\output_NPlesant_Custom_deg1_esa.txt' + "\n"
        filelines[82] = sim_folder + r'\output_NPlesant_Custom_deg2_esa.txt' + "\n"

        # copy, write out file
        this_vvwm = open(new_file, "w")
        this_vvwm.writelines(filelines)
        this_vvwm.close()

        # run vvwm.exe (vvwm.exe "inputfilename")
        command = new_exe + " " + new_file
        print(command)
        subprocess.call(command)


