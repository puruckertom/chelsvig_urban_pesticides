# --------------------------------------------------
# declare most _file and _path variables
# prevent all scripts from being run from outside of the \src folder
# --------------------------------------------------

import os
#from prpy_bookkeeping import *

# if any([os.path.basename(os.path.abspath(os.curdir)) != 'src', os.path.basename(os.path.dirname(os.path.abspath(os.curdir))) != 'chelsvig_urban_pesticides']):
#     logging.error("Error! You must first navigate to <chelsvig_urban_pesticides/probabilistic_python/src> in order to run this file.")
#     print("Error! You must first navigate to <chelsvig_urban_pesticides/src> in order to run this file.")
#     exit()

main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dir_path = main_path + r'\probabilistic_python'
exe_path = dir_path + r'\exe'
swmm_path = dir_path + r'\input\swmm'
inp_path = dir_path + r'\input\swmm\NPlesantCreek.inp'
bin_path = dir_path + r'\input\swmm\NPlesantCreek.out'
vvwm_path = dir_path + r'\input\vvwm'
wet_path = dir_path + r'\weather'

print("main_path  ",main_path)
print("dir_path   ",dir_path)
print("exe_path   ",exe_path)
print("swmm_path  ",swmm_path)
print("inp_path   ",inp_path)
print("bin_path   ",bin_path)
print("vvwm_path  ",vvwm_path)
print("wet_path   ",wet_path)