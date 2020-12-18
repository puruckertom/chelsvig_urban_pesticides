import time
start = time.process_time()

# run 1-5 minus 01d and 01e
script = "01a"
rds01a = __import__('01a_run_determ_swmm')
script = "01b"
rwsof01b = __import__('01b_read_write_swmm_output_file')
script = "01c"
svf01c = __import__('01c_setup_vvwm_files')

# Here is the point where we start simulating. Turn it up from 5 sims to 1000 sims
nsims = 50
script = "02"
lps02 = __import__('02_lhs_param_swmm')
script = "03"
rwsif03 = __import__('03_read_write_swmm_input_file')
script = "04"
rps04 = __import__('04_run_prob_swmm')
script = "05"
rwsof05 = __import__('05_read_write_swmm_output_file')

# report runtime
total_seconds = time.process_time() - start
hours = total_seconds//3600
minutes = (total_seconds%3600)//60
seconds = round(total_seconds%60)

print("Total Runtime:", hours, "hours,", minutes, "minutes, and", seconds, "seconds.")
