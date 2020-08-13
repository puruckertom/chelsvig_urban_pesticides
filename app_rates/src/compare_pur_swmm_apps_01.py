# ------------------------------------------------------------------------------------------
# read swmm .rpt output file, and store desired outputs
# ------------------------------------------------------------------------------------------

# setup
import shutil

# specify locations
dir_path = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\probabilistic_python'

swmm_path = dir_path + r'\input\swmm'
print(swmm_path)
swmm_file = swmm_path + r'\NPlesantCreek.rpt'
print(swmm_file)
inp_file = swmm_path + r'\NPlesantCreek.inp'
print(inp_file)
vvwm_path = dir_path + r'\input\vvwm'
print(vvwm_path)

outfalls = ['\outfall_31_26']

# read in the .inp file subcatchment areas (to use later in script)
# read the .inp file
file = open(inp_file, "r")

# create blank list to hold subcatchment areas
sub_list_area = []

# skip x lines
lines1 = file.readlines()[55:]

for thissub in range(0, 113):
    # grab the area
    thisline = lines1[thissub]
    fixline = " ".join(thisline.split())
    listline = fixline.split()
    area = listline[3]
    area = float(area)

    # insert into blank list
    sub_list_area.append(area)

with open(r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\app_rates\io\swmm_sub_list_areas.txt', 'w') as f:
    for item in sub_list_area:
        f.write("%s\n" % item)

# grab the previously computed daily averages of swmm outputs
original = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\probabilistic_python\input\swmm\swmm_output_davg_runf.csv'
target = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\app_rates\io\swmm_output_davg_runf.csv'
shutil.copyfile(original, target)

original = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\probabilistic_python\input\swmm\swmm_output_davg_bif.csv'
target = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\app_rates\io\swmm_output_davg_bif.csv'
shutil.copyfile(original, target)

# grab the previously computed converted daily averages of swmm outputs
original = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\probabilistic_python\input\swmm\swmm_conv_to_vvwm_runf.csv'
target = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\app_rates\io\swmm_conv_to_vvwm_runf.csv'
shutil.copyfile(original, target)

original = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\probabilistic_python\input\swmm\swmm_conv_to_vvwm_bif.csv'
target = r'C:\Users\echelsvi\git\chelsvig_urban_pesticides\app_rates\io\swmm_conv_to_vvwm_bif.csv'
shutil.copyfile(original, target)
