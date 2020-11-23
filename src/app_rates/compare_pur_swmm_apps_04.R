# setup
library(ggplot2)
# library(gtable)
# library(lubridate)
library(dplyr)

source("path_names_ar.R")

figs <- paste0(main_dir,"app_rates/figures/") #JMS 9/22/20
dir_weather <- paste0(main_dir,"probabilistic_python/weather/") #JMS 9/22/20

# -------------------------------------------------
# function for making cumsum scatter plots
#--------------------------------------------------
make_cs_scatter_plot <- function(i){
  percent_develop1 <- 0
  p <- read.csv(file = paste0(main_dir,'app_rates/output/bug_values_sub', i, '.csv'), stringsAsFactors = F) %>%
    mutate(
      # fix 'dates' column type
      dates = as.Date(dates,"%m/%d/%Y"),
      # hectares of developed land use in the subcatchment
      sub_develop_ha = sub_area_ha * sub_perc_develop,
      # total kg that should be applied to the sub, based on its urban ha
      pur_app_for_sub_kg = pur_app_kgha * sub_area_ha * sub_perc_develop) %>% 
    (function(df){ percent_develop1 <<- round((df[1,12]*100), 2)
    return(df) }) %>% select(dates, pur_app_for_sub_kg, totl_bif_n_runf_kg) %>% 
    mutate(pur_app_for_sub_kg = cumsum(pur_app_for_sub_kg),
           totl_bif_n_runf_kg = cumsum(totl_bif_n_runf_kg)) %>% 
    #reshape2::melt(id.var='dates') %>% 
    ggplot(mapping = aes(x=pur_app_for_sub_kg, y=totl_bif_n_runf_kg, 
                         col = (pur_app_for_sub_kg>=totl_bif_n_runf_kg))) +
    geom_point() + geom_abline(slope = 1, intercept = 0) +
    ggtitle(paste0("Bifenthrin Applied vs Bifenthrin in Runoff (Cummulative) for Subcatchment ",
                   i, "(", percent_develop1, "% developed)")) 
  return(p)
}
# ------------------------------------------------------

# Make some plots for finding the over estimation bug

# Kilograms
pdf(paste(figs,"find_bug_cs_scatter.pdf",sep=""),width=11,height=8, onefile=TRUE)

for(i in 1:113){
  print(make_cs_scatter_plot(i)) #(functionized) -JMS 9/23/20
}
dev.off()

#######################################

# now plot them all on one plot

add_cs_scatter_plot <- function(i){
  percent_develop1 <- 0
  p <- read.csv(file = paste0(main_dir,'app_rates/output/bug_values_sub', i, '.csv'), stringsAsFactors = F) %>%
    mutate(
      # fix 'dates' column type
      dates = as.Date(dates,"%m/%d/%Y"),
      # hectares of developed land use in the subcatchment
      sub_develop_ha = sub_area_ha * sub_perc_develop,
      # total kg that should be applied to the sub, based on its urban ha
      pur_app_for_sub_kg = pur_app_kgha * sub_area_ha * sub_perc_develop) %>%
    select(dates, pur_app_for_sub_kg, totl_bif_n_runf_kg) %>% 
    mutate(pur_app_for_sub_kg = cumsum(pur_app_for_sub_kg),
           totl_bif_n_runf_kg = cumsum(totl_bif_n_runf_kg)) %>% 
    #reshape2::melt(id.var='dates') %>% 
    geom_point(mapping = aes(x=pur_app_for_sub_kg, y=totl_bif_n_runf_kg, 
                         col = (pur_app_for_sub_kg>=totl_bif_n_runf_kg)))
  return(p)
}

# Make some plots for finding the over estimation bug

# Kilograms
pdf(paste(figs,"find_bug_1cs_scatter.pdf",sep=""),width=11,height=8, onefile=TRUE)

oneP <- 
  ggplot(xlim = c(0,175), ylim = c(0,310)) + 
  geom_abline(slope = 1, intercept = 0) +
  ggtitle(paste0("Bifenthrin Applied vs Bifenthrin in Runoff (Cummulative)"))
  
for(i in 1:113){
  oneP <- oneP + add_cs_scatter_plot(i)
}
print(oneP)
dev.off()

#######################################

# now get the 10 most and least buggy subcatchments.
get_bugginess <- function(i){
  df <- read.csv(file = paste0(main_dir,'app_rates/output/bug_values_sub', i, '.csv'), stringsAsFactors = F) %>%
    mutate(
      # fix 'dates' column type
      dates = as.Date(dates,"%m/%d/%Y"),
      # hectares of developed land use in the subcatchment
      sub_develop_ha = sub_area_ha * sub_perc_develop,
      # total kg that should be applied to the sub, based on its urban ha
      pur_app_for_sub_kg = pur_app_kgha * sub_area_ha * sub_perc_develop) %>% 
    select(dates, pur_app_for_sub_kg, totl_bif_n_runf_kg) %>% 
    mutate(pur_app_for_sub_kg = cumsum(pur_app_for_sub_kg),
           totl_bif_n_runf_kg = cumsum(totl_bif_n_runf_kg),
           logical = (pur_app_for_sub_kg>=totl_bif_n_runf_kg))
  return(mean(df$logical))
}

bugginess <- sapply(1:113,get_bugginess)

top10buggiest <- order(bugginess)[1:10]
top10leastbuggy <- rev(order(bugginess)[103:112])
