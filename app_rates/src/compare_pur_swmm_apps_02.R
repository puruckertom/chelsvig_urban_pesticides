# ------------------------------------------------------------------------------
# trying to find the runoff and bifenthrin concentration bug (swmm -> vvwm)
# ------------------------------------------------------------------------------



# -----------------------------------------------------------
# read in daily application rates (kg/ha)
apps <- read.table('C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/calpip/app_rate_output_for_swmm.txt',
                       sep="\t", skip=3, col.names=c("date", "hour", "app_daily_kgha"))


# compute daily applications (kg)
apps$app_daily_kg <- apps$app_daily_kgha*6485.67 # <- hectares of urban land use in PGC
apps <- apps[-1,]

# ^ above external time series for developed land use % for each subcatchment (I think)
# and, each subcatchment as an area provided (ha), so maybe the application rate gets
# multiplied by the kg/ha to get kg applied to that subcatchment...?
# -----------------------------------------------------------



# -----------------------------------------------------------
# read in swmm subcatchment areas (ha)
subcatch_areas <- read.table('C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/io/swmm_sub_list_areas.txt', 
                             sep=" ", header=F, col.names="area_ha")
# -----------------------------------------------------------



# -----------------------------------------------------------
# read in subcatchment land use percentages
# -----------------------------------------------------------
# need to get from .inp file
subcatch_landuse <- read.csv('C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/io/sub_list_landuse.csv',sep=",", header=T)



# -----------------------------------------------------------
# read in swmm runoff output (generated in .rpt), units = cms
swmm_rpt_runf <- read.csv('C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/io/swmm_output_runf.csv',sep=",", header=T)
swmm_rpt_runf <- swmm_rpt_runf[,-1 ]

# read in swmm bif output (generated in .rpt), units = ug/l
swmm_rpt_bif <- read.csv('C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/io/swmm_output_bif.csv',sep=",", header=T)
swmm_rpt_bif <- swmm_rpt_bif[,-1 ]
# -----------------------------------------------------------


# -----------------------------------------------------------
# read in swmm converted runoff values (to be input into vvwm), units = cm/ha/day
swmm_conv_runf <- read.csv('C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/io/swmm_runf_conv_for_vvwm.csv',sep=",", header=T)
swmm_conv_runf <- swmm_conv_runf[,-1 ]

# read in swmm converted bif values (to be input into vvwm), units = g/ha/day
swmm_conv_bif <- read.csv('C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/io/swmm_bif_conv_for_vvwm.csv',sep=",", header=T)
swmm_conv_bif <- swmm_conv_bif[,-1 ]
# -----------------------------------------------------------


# -----------------------------------------------------------
# create output files that contain all relative runf,bif values for each subcatchment
# for each subcatchment
for (sub in 1:113){
  # create blank df
  output_df <- data.frame(matrix(ncol = 1, nrow = dim(swmm_rpt_runf)[1]))
  
  # fill blank df with needed cols
  output_df$dates <- seq(from=as.Date("2009-01-02"), to = as.Date("2017-12-31"), by = "day")
  output_df$pur_app_kg <- apps$app_daily_kg
  output_df$pur_app_kgha <- apps$app_daily_kgha
  output_df$rpt_runf_cms <- swmm_rpt_runf[,sub]
  output_df$conv_runf_cmha <- swmm_conv_runf[,sub]
  output_df$rpt_bif_ugl <- swmm_rpt_bif[,sub]
  output_df$conv_bif_gha <- swmm_conv_bif[,sub]
  
  output_df$runf_cmd <- output_df$rpt_runf_cms*86400
  output_df$bif_ugcm <- swmm_rpt_bif[,sub]*1000
  output_df$totl_bif_n_runf_kg <- (output_df$runf_cmd * output_df$bif_ugcm) / 1e9
  
  output_df$sub_area_ha <- rep(subcatch_areas[sub,1], times=dim(swmm_rpt_runf)[1])
  output_df$sub_perc_develop <- rep(subcatch_landuse[sub,1], times=dim(swmm_rpt_runf)[1])
  
  output_df <- output_df[,-1]

  write.csv(output_df, file=paste0(file='C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/output/', "bug_values_sub", sub, ".csv", sep=""), row.names=F)
   
}
# -----------------------------------------------------------




# -----------------------------------------------------------
# analyze the data

# !! this is *just* looking at a random subcatchment (85)
df <- read.csv(file='C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/output/bug_values_sub85.csv', header=T)
toobig <- df[which(df$totl_bif_n_runf_kg > df$pur_app_kg),]
dim(toobig)


# things to talk about:
#   the pur_app_kg col is the total kg of bifenthrin for PGC's entire urban area.


# -----------------------------------------------------------







