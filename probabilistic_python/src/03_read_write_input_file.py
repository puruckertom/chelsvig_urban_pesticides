# -----------------------------------------
# read, write, input file
# -----------------------------------------

# setup
import pytest_shutil, shutil, os


# define root path for all folders
root_path = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\probabilistic_python\input\swmm'
print(os.path.exists(root_path))

# todo create loop that will do this nsims times

# create new folder location
folder = 'input_01'
folder_path = os.path.join(root_path, folder)

if not os.path.exists(folder_path):
    os.mkdir(folder_path)
    print("Folder ", folder , " created ")
else:
    print("Folder ", folder , " already exists ")

print(os.path.exists(folder_path))

# copy base .inp and put in new folder
base_inp = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\probabilistic_python\input\swmm\NPlesantCreek.inp'
shutil.copy(base_inp, folder_path)

# todo edit the newly-copied .inp with the lhs params
