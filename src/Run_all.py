##----------------------------
# One script to rule the all!!!
##----------------------------
import time
start = time.process_time()

script = "01a"
rds01a = __import__('01a_run_determ_swmm')
script = "01b"
rwsof01b = __import__('01b_read_write_swmm_output_file')
script = "01c"
svf01c = __import__('01c_setup_vvwm_files')
script = "01d"
rdv01d = __import__('01d_run_determ_vvwm')
script = "01e"
pofp01e = __import__('01e_prep_outputs_for_plots')
script = "02"
lps02 = __import__('02_lhs_param_swmm')
script = "03"
rwsif03 = __import__('03_read_write_swmm_input_file')
script = "04"
rps04 = __import__('04_run_prob_swmm')
script = "05"
rwsof05 = __import__('05_read_write_swmm_output_file')
script = "06"
svf06 = __import__('06_setup_vvwm_files')
script = "07"
lpv07 = __import__('07_lhs_param_vvwm')
script = "08"
rwvif08 = __import__('08_read_write_vvwm_input_file')
script = "09"
rpv09 = __import__('09_run_prob_vvwm')
script = "10"
pofp10 = __import__('10_prep_outputs_for_plots')

print(time.process_time() - start)