##----------------------------
# One script to rule the all!!!
##----------------------------
import time
start = time.process_time()

rds01a = __import__('01a_run_determ_swmm')
rwsof01b = __import__('01b_read_write_swmm_output_file')
svf01c = __import__('01c_setup_vvwm_files')
rdv01d = __import__('01d_run_determ_vvwm')
pofp01e = __import__('01e_prep_outputs_for_plots')
lps02 = __import__('02_lhs_param_swmm')
rwsif03 = __import__('03_read_write_swmm_input_file')
rps04 = __import__('04_run_prob_swmm')
rwsof05 = __import__('05_read_write_swmm_output_file')
svf06 = __import__('06_setup_vvwm_files')
lpv07 = __import__('07_lhs_param_vvwm')
rwvif08 = __import__('08_read_write_vvwm_input_file')
rpv09 = __import__('09_run_prob_vvwm')
pofp10 = __import__('10_prep_outputs_for_plots')

print(time.process_time() - start)