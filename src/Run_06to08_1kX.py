import time
start = time.process_time()

nsims = 1000

# run 6-8
script = "06"
svf06 = __import__('06_setup_vvwm_files')
script = "07"
lpv07 = __import__('07_lhs_param_vvwm')
script = "08"
rwvif08 = __import__('08_read_write_vvwm_input_file')

# report runtime
total_seconds = time.process_time() - start
hours = total_seconds//3600
minutes = (total_seconds%3600)//60
seconds = round(total_seconds%60)

print("Total Runtime:", hours, "hours,", minutes, "minutes, and", seconds, "seconds.")
