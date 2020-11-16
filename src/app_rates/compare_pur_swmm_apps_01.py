# ------------------------------------------------------------------------------------------
# read swmm .rpt output file, and store desired outputs
# ------------------------------------------------------------------------------------------

# setup
import shutil, os

# if any([os.path.basename(os.path.abspath(os.curdir)) != 'src', os.path.basename(os.path.dirname(os.path.abspath(os.curdir))) != 'app_rates']):
#     print("Error! You must first navigate to <chelsvig_urban_pesticides/app_rates/src> in order to run this file.")
#     exit()

# main_dir = os.path.abspath("../..") #JMS 9/30/20
main_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# specify locations
# prpy_dir = main_dir + r'\probabilistic_python' #JMS 9/23/20

# swmm_dir = prpy_dir + r'\input\swmm'
# print(r'swmm_dir:  ', swmm_dir) #JMS 9/23/20
# swmm_rpt_path = swmm_dir + r'\NPlesantCreek.rpt'
# print(r'swmm_rpt_path:  ', swmm_rpt_path) #JMS 9/23/20
swmm_inp_path = main_dir + r'\probabilistic_python\input\swmm\NPlesantCreek.inp' #swmm_dir + r'\NPlesantCreek.inp' -JMS 10-27-20
print(r'swmm_inp_path:  ', swmm_inp_path) #JMS 9/23/20
# vvwm_path = prpy_dir + r'\input\vvwm'
# print(r'vvwm_path:  ', vvwm_path) #JMS 9/23/20

# outfalls = ['\outfall_31_26']

# read in the .inp file subcatchment areas (to use later in script)
# read the .inp file
ip_file = open(swmm_inp_path, "r") #JMS 9/23/20

# skip x lines
lines1 = ip_file.readlines()[55:] #JMS 9/23/20

# close .inp file
ip_file.close() #JMS 9/23/20

# make a list of subcatchment areas
sub_list_area = [lines1[thissub].split()[3] for thissub in range(113)]  #JMS 9/23/20

# write list to .txt file for later use
with open(main_dir + r'\app_rates\io\swmm_sub_list_areas.txt', 'w') as f: #JMS 9/23/20
    f.write("\n".join(sub_list_area)) #JMS 9/23/20

# grab the previously computed daily averages of swmm outputs
original = main_dir + r'\probabilistic_python\input\swmm\swmm_output_davg_runf.csv' #JMS 9/23/20
target = main_dir + r'\app_rates\io\swmm_output_davg_runf.csv' #JMS 9/23/20
shutil.copyfile(original, target)

original = main_dir + r'\probabilistic_python\input\swmm\swmm_output_davg_bif.csv' #JMS 9/23/20
target = main_dir + r'\app_rates\io\swmm_output_davg_bif.csv' #JMS 9/23/20
shutil.copyfile(original, target)

# grab the previously computed converted daily averages of swmm outputs
original = main_dir + r'\probabilistic_python\input\swmm\swmm_conv_to_vvwm_runf.csv' #JMS 9/23/20
target = main_dir + r'\app_rates\io\swmm_conv_to_vvwm_runf.csv' #JMS 9/23/20
shutil.copyfile(original, target)

original = main_dir + r'\probabilistic_python\input\swmm\swmm_conv_to_vvwm_bif.csv' #JMS 9/23/20
target = main_dir + r'\app_rates\io\swmm_conv_to_vvwm_bif.csv' #JMS 9/23/20
shutil.copyfile(original, target)