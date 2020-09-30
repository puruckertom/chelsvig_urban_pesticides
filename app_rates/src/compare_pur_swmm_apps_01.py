# ------------------------------------------------------------------------------------------
# read swmm .rpt output file, and store desired outputs
# ------------------------------------------------------------------------------------------

# setup
import shutil, os
mypath = os.path.abspath("../..") #JMS 9/30/20

# specify locations
dir_path = mypath + r'\probabilistic_python' #JMS 9/23/20

swmm_path = dir_path + r'\input\swmm'
print(r'swmm_path:  ', swmm_path) #JMS 9/23/20
swmm_file = swmm_path + r'\NPlesantCreek.rpt'
print(r'swmm_file:  ', swmm_file) #JMS 9/23/20
inp_file = swmm_path + r'\NPlesantCreek.inp'
print(r'inp_file:  ', inp_file) #JMS 9/23/20
vvwm_path = dir_path + r'\input\vvwm'
print(r'vvwm_path:  ', vvwm_path) #JMS 9/23/20

outfalls = ['\outfall_31_26']

# read in the .inp file subcatchment areas (to use later in script)
# read the .inp file
ipfile = open(inp_file, "r") #JMS 9/23/20

# skip x lines
lines1 = ipfile.readlines()[55:] #JMS 9/23/20

# close .inp file
close(ipfile) #JMS 9/23/20

# make a list of subcatchment areas
sub_list_area = [lines1[thissub].split()[3] for thissub in range(113)]  #JMS 9/23/20

# write list to .txt file for later use
with open(mypath + r'\app_rates\io\swmm_sub_list_areas.txt', 'w') as f: #JMS 9/23/20
    f.write("\n".join(sub_list_area)) #JMS 9/23/20

# grab the previously computed daily averages of swmm outputs
original = mypath + r'\probabilistic_python\input\swmm\swmm_output_davg_runf.csv' #JMS 9/23/20
target = mypath + r'\app_rates\io\swmm_output_davg_runf.csv' #JMS 9/23/20
shutil.copyfile(original, target)

original = mypath + r'\probabilistic_python\input\swmm\swmm_output_davg_bif.csv' #JMS 9/23/20
target = mypath + r'\app_rates\io\swmm_output_davg_bif.csv' #JMS 9/23/20
shutil.copyfile(original, target)

# grab the previously computed converted daily averages of swmm outputs
original = mypath + r'\probabilistic_python\input\swmm\swmm_conv_to_vvwm_runf.csv' #JMS 9/23/20
target = mypath + r'\app_rates\io\swmm_conv_to_vvwm_runf.csv' #JMS 9/23/20
shutil.copyfile(original, target)

original = mypath + r'\probabilistic_python\input\swmm\swmm_conv_to_vvwm_bif.csv' #JMS 9/23/20
target = mypath + r'\app_rates\io\swmm_conv_to_vvwm_bif.csv' #JMS 9/23/20
shutil.copyfile(original, target)