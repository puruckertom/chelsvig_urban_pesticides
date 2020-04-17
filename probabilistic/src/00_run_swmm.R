# --------------------------------------------------------------------------
# SWMM probabilistic sensitivity analysis
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# run everything - only once everything is ready to go!
# --------------------------------------------------------------------------


# set up local environment
source(paste(swmmdir,"src/01_load_environment.R",sep = ""))


# set up swmm and visualize .inp file
source(paste(swmmdir,"src/02_setup_swmm_and_visualize_inp.R",sep = ""))

# parameterize inputs
source(paste(swmmdir,"src/03_lhs_parameterization.R",sep = ""))


# conduct simulations by: re-write, update, run swmm with LHS parameters
source(paste(swmmdir,"src/04_write_update_run_swmm.R",sep = ""))


# #create input dataframe
# #source(paste(pwcdir,"src/03write_input_dataframe.R",sep = ""))
# # read text,csv files and save results into dataframe
# source(paste(pwcdir,"src/04_write_ouput_into_df.R",sep = ""))
# 
# # load input and output objects into environment
# source(paste(pwcdir,"src/05load_io.R",sep = ""))


# run sensitivity analysis on time daily arrays
source(paste(pwcdir,"src/06daily_sensitivity_analysis_linear.R",sep = ""))

#
source(paste(pwcdir,"src/06Max_sensitivity_analysis_linear.R",sep = ""))

# plot results
source(paste(pwcdir,"src/07sensitivity_analyses_graphics.R",sep = ""))
source(paste(pwcdir,"src/08pardistribution.R",sep = ""))



# --------------------------------------------------------------------------
# the end
# --------------------------------------------------------------------------