# -------------------------------------------------
# examine deterministic outputs
# -------------------------------------------------


# read in data


# specify location
Sys.info()
Sys.info()[4]

if(Sys.info()[4]=="LZ2626UECHELSVI"){
  maindir <- "C:/Users/echelsvi/git/chelsvig_urban_pesticides/"
}

swmm_path <- paste0(maindir, 'probabilistic_python/input/swmm')
vvwm_path <- paste0(maindir, 'probabilistic_python/input/vvwm')

outfalls <- c('/outfall_31_26', '/outfall_31_28', '/outfall_31_29', 
              '/outfall_31_35','/outfall_31_36', '/outfall_31_38', '/outfall_31_42')


# plot: water column concentrations

o <- '/outfall_31_26'
#for o in outfalls{

  # determinstic - water column concentration
  # set pathways
  outfall_path <- paste0(vvwm_path, o)
  determ <- paste0(outfall_path, '/determ')
  vvwm_out <- paste0(determ, '/output_NPlesant_Custom_parent_daily.csv')
  swmm_out <- paste0(determ, '/output.zts')

  # read csv
  v_output <- read.csv(vvwm_out, skip=5, header=F)
  names(v_output) <- c("depth_m", "water_col_conc_kgm3", "benth_conc_kgm3", "peak_water_conc_kgm3")
  v_output$date <- seq(as.Date("2009-01-01"), as.Date("2017-12-31"), by="days")#format 1961-01-01
  
  # subset desired cols, convert units
  plot_vvwm <- v_output[, c("date", "water_col_conc_kgm3", "benth_conc_kgm3")]
  plot_vvwm$water_col_conc_ugml <- plot_vvwm$water_col_conc_kgm3*1000000
  plot_vvwm$benth_conc_ugml <- plot_vvwm$benth_conc_kgm3*1000000
  plot_vvwm <- plot_vvwm[, c("date", "water_col_conc_ugml", "benth_conc_ugml")]
  
  # remove outliers
  vvwm_outlier <- plot_vvwm[-c(1609), ] # 1.95e15
  vvwm_outlier <- vvwm_outlier[-c(2272),] # 6.2372e14
  
  # quick plot
  plot(vvwm_outlier$water_col_conc_ugml, type="l")
  plot(plot_vvwm$water_col_conc_ugml, type="l")
  
  
  # determinstic - benthic zone concentration
  # quick plot
  plot(plot_vvwm$benthic_conc_ugml, type="l")
  

  
  
  
  
  
  
  
  
  
  
  
  
  
  