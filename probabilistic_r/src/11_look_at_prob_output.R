# -------------------------------------------------
# look at prob and determ outputs
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
determ_path <- paste0(outfall_path, '/determ')
det_v <- paste0(determ, '/output_NPlesant_Custom_parent_daily.csv')
det_s <- paste0(determ, '/output.zts')

# read csv
determ_v <- read.csv(det_v, skip=5, header=F)
names(determ_v) <- c("depth_m", "water_col_conc_kgm3", "benth_conc_kgm3", "peak_water_conc_kgm3")
determ_v$date <- seq(as.Date("2009-01-01"), as.Date("2017-12-31"), by="days")#format 1961-01-01

# subset desired cols, convert units
plot_determ <- determ_v[, c("date", "water_col_conc_kgm3", "benth_conc_kgm3")]
plot_determ$water_col_conc_ugml <- plot_determ$water_col_conc_kgm3*1000000
plot_determ$benth_conc_ugml <- plot_determ$benth_conc_kgm3*1000000
plot_determ <- plot_determ[, c("date", "water_col_conc_ugml", "benth_conc_ugml")]

# remove outliers
plot_determ2 <- plot_determ[-c(1609), ] # 1.95e15
plot_determ2 <- plot_determ2[-c(2272),] # 6.2372e14

# quick plot - water column concentration
plot(plot_determ2$water_col_conc_ugml, type="l") #w/o outliers
plot(plot_determ$water_col_conc_ugml, type="l") #w/ outlieres


# quick plot - benthic zone concentration
plot(plot_determ$benthic_conc_ugml, type="l")

















