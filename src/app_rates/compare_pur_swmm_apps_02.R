# ------------------------------------------------------------------------------
# trying to find the runoff and bifenthrin concentration bug (swmm -> vvwm)
# ------------------------------------------------------------------------------

source("path_names_ar.R")

# -----------------------------------------------------------

# new {
library(dplyr)

# read in daily application rates (kg/ha)
apps <- read.table(paste0(main_dir,'app_rates/calpip/app_rate_output_for_swmm_48rain.txt'),
                   sep="\t", col.names=c("dates", "hour", "pur_app_kgha")) %>% 
  # compute daily applications (kg)
  mutate(pur_app_kg = pur_app_kgha*6485.67)
# } 10/27/20

# # read in daily application rates (kg/ha)
# apps <- read.table(paste0(main_dir,'app_rates/calpip/app_rate_output_for_swmm_48rain.txt'),  #JMS 9/22/20
#                        sep="\t", skip=0, col.names=c("date", "hour", "app_daily_kgha")) #JMS 9/23/20
# ## Why does it skip the first three days???? -JMS 9/23/20
# 
# # compute daily applications (kg)
# apps$app_daily_kg <- apps$app_daily_kgha*6485.67 # <- hectares of urban land use in PGC

# ^ above external time series for developed land use % for each subcatchment (I think)
# and, each subcatchment as an area provided (ha), so maybe the application rate gets
# multiplied by the kg/ha to get kg applied to that subcatchment...?
# -----------------------------------------------------------



# -----------------------------------------------------------
# read in swmm subcatchment areas (ha)
subcatch_areas <- read.table(paste0(main_dir,'app_rates/io/swmm_sub_list_areas.txt'), 
                             sep=" ", header=F, col.names="area_ha") #JMS 9/22/20
# -----------------------------------------------------------



# -----------------------------------------------------------
# read in subcatchment land use percentages
# -----------------------------------------------------------
# need to get from .inp file
subcatch_landuse <- read.csv(paste0(main_dir,'app_rates/io/sub_list_landuse.csv'),
                             sep=",", header=T, nrows = 113) #JMS 10/27/20

# -----------------------------------------------------------
# read in swmm runoff output (generated in .rpt), units = cms
swmm_rpt_runf <- read.csv(paste0(main_dir,'app_rates/io/swmm_output_davg_runf.csv'),
                          sep=",", header=T)[,-1 ]

# read in swmm bif output (generated in .rpt), units = ug/l
swmm_rpt_bif <- read.csv(paste0(main_dir,'app_rates/io/swmm_output_davg_bif.csv'),
                         sep=",", header=T)[,-1 ]
# -----------------------------------------------------------


# -----------------------------------------------------------
# read in swmm converted runoff values (to be input into vvwm), units = cm/ha/day
swmm_conv_runf <- read.csv(paste0(main_dir,'app_rates/io/swmm_conv_to_vvwm_runf.csv'),
                           sep=",", header=T)[,-1 ]

# read in swmm converted bif values (to be input into vvwm), units = g/ha/day
swmm_conv_bif <- read.csv(paste0(main_dir,'app_rates/io/swmm_conv_to_vvwm_bif.csv'),
                          sep=",", header=T)[,-1 ]
# -----------------------------------------------------------


output_df <- apps %>% select(-hour) %>% 
  cbind((stack(swmm_rpt_runf) %>% transmute(sub=as.integer(ind), rpt_runf_cms=values)),
        conv_runf_cmha = stack(swmm_conv_runf)$values,
        rpt_bif_ugl = stack(swmm_rpt_bif)$values,
        conv_bif_gha = stack(swmm_conv_bif)$values) %>% 
  mutate(runf_cmd = rpt_runf_cms*86400,
         bif_ugcm = rpt_bif_ugl*1000,
         totl_bif_n_runf_kg = rpt_runf_cms*rpt_bif_ugl*0.0864) %>%
  inner_join(data.frame(sub=1:113, 
                        sub_area_ha=subcatch_areas$area_ha, 
                        sub_perc_develop=subcatch_landuse$developed_pct)) 

write_sub <- function(i){
  select(filter(output_df, sub==i), -sub) %>% write.csv(
    file=paste0(main_dir,"app_rates/output/bug_values_sub",i,".csv"), row.names=F)
  i
}
sapply(1:113, write_sub)

# for (i in 1:113){
#   filter(output_df, sub==i) %>% write.csv(
#     file=paste0(main_dir,"app_rates/output/bug_values_sub",i,".csv"), row.names=F)
# }

# -----------------------------------------------------------
# create output files that contain all relative runf, bif values for each subcatchment
# for each subcatchment
# for (sub in 1:113){
#   # create df: start with date column -JMS 9/23/20
#   output_df <- data.frame(dates = seq(from=as.Date("2009-01-01"), to = as.Date("2017-12-31"), by = "day")) #JMS 9/23/20
#   
#   # add other columns needed -JMS 9/23/20
#   output_df$pur_app_kg <- apps$app_daily_kg
#   output_df$pur_app_kgha <- apps$app_daily_kgha
#   output_df$rpt_runf_cms <- swmm_rpt_runf[,sub]
#   output_df$conv_runf_cmha <- swmm_conv_runf[,sub]
#   output_df$rpt_bif_ugl <- swmm_rpt_bif[,sub]
#   output_df$conv_bif_gha <- swmm_conv_bif[,sub]
#   
#   output_df$runf_cmd <- output_df$rpt_runf_cms*86400
#   output_df$bif_ugcm <- swmm_rpt_bif[,sub]*1000
#   output_df$totl_bif_n_runf_kg <- (output_df$runf_cmd * output_df$bif_ugcm) / 1e9
#   
#   output_df$sub_area_ha <- rep(subcatch_areas[sub,1], times=dim(swmm_rpt_runf)[1])
#   output_df$sub_perc_develop <- rep(subcatch_landuse[sub,1], times=dim(swmm_rpt_runf)[1])
#   
#   write.csv(output_df, file=paste0(main_dir,'app_rates/output/bug_values_sub', sub, ".csv"), row.names=F) #JMS 9/22/20
#    
# }
# -----------------------------------------------------------




# -----------------------------------------------------------
# analyze the data

# !! this is *just* looking at a random subcatchment (85)
df <- read.csv(file=paste0(main_dir,'app_rates/output/bug_values_sub85.csv'), header=T) # JMS 9/22/20
toobig <- df[which(df$totl_bif_n_runf_kg > df$pur_app_kg),]
dim(toobig)


# things to talk about:
#   the pur_app_kg col is the total kg of bifenthrin for PGC's entire urban area.


# -----------------------------------------------------------







