# --------------------------------------------------
# declare most _file and _path variables
# prevent all scripts from being run from outside of the \src folder
# --------------------------------------------------

import os

if os.path.basename(os.path.abspath(os.curdir)) != 'src':
    print("Error! You must first navigate to <chelsvig_urban_pesticides/probabilistic_python/src> in order to run this file.")
    exit()

main_path = os.path.abspath("../..")
dir_path = os.path.abspath("..")
exe_path = dir_path + r'\exe'
swmm_path = dir_path + r'\input\swmm'
inp_path = dir_path + r'\input\swmm\NPlesantCreek.inp'
bin_path = dir_path + r'\input\swmm\NPlesantCreek.out'
vvwm_path = dir_path + r'\input\vvwm'
wet_path = dir_path + r'\weather'

# print(main_path)
# print(dir_path)
# print(exe_path)
# print(swmm_path)
# print(inp_path)
# print(bin_path)
# print(vvwm_path)
# print(wet_path)