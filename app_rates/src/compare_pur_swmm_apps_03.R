# ---------------------------------------------------------------
# visually examine swmm bifenthrin loadings
# ---------------------------------------------------------------

# setup
library(ggplot2)
library(gtable)
library(lubridate)
library(dplyr)

figs <- "C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/figures/"
dir_weather <- "C:/Users/echelsvi/git/chelsvig_urban_pesticides/probabilistic_python/weather/"


# ------------------------------------------------------
# Kilograms
pdf(paste(figs,"find_bug_kg_urban.pdf",sep=""),width=11,height=8, onefile=TRUE)

for(i in 1:113){

  # read in data
  data <- read.csv(file=paste0('C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/output/bug_values_sub', i, '.csv', sep=''))
  data$dates <- seq(from=as.Date("2009-01-01"), to = as.Date("2017-12-31"), by = "day")
  
  # create a few new cols to analyze
  data$sub_develop_ha <- data$sub_area_ha*data$sub_perc_develop # hectares of developed land use in the subcatchment
  data$pur_app_for_sub_kg <- data$pur_app_kgha*data$sub_develop_ha # total kg that should be applied to the sub, based on its urban ha
  
  if (data$sub_perc_develop[1] == 0){
    data$pur_app_for_sub_kg <- rep(0, times=dim(data)[1])
  }
  
  # to use with plot title
  percent_develop <- round((data[1,12]*100), 2)
  
  # subset
  data <- data[, c("dates", "pur_app_for_sub_kg", "totl_bif_n_runf_kg")]
  
  # cumulative sum
  for (r in 2:dim(data)[1]){
    data[r,2] <- data[r-1,2] + data[r,2]
    data[r,3] <- data[r-1,3] + data[r,3]
  }
  
  # melt for plotting
  data_melt <- reshape2::melt(data, id.var='dates')
  head(data_melt)
  
  p <- ggplot(data_melt, aes(x=dates, y=value, col=variable)) + 
    geom_line() +
    xlab("")+
    ylab("Kilograms")+
    ggtitle(paste0("Cumulative Bifenthrin Applied to Urban Hectares for Subcatchment ", i, "(", percent_develop, "% developed)", sep=''))
  print(p)
}
dev.off()

# ------------------------------------------------------
# Precipitation
pdf(paste(figs,"find_bug_precip.pdf",sep=""),width=11,height=8)

# read in weather file, make necessary edits
precip <- read.csv(file=paste0(dir_weather, "Precipitation_nldas_daily.csv", sep=""), header=TRUE, sep=",")
precip <- precip[1:3287, ]
precip$date <- seq(as.Date("2009-01-01"), as.Date("2017-12-31"), by="days")
precip$DailyTotal_kgm2 <- as.numeric(levels(precip$DailyTotal_kgm2))[precip$DailyTotal_kgm2]
precip$DailyTotal_cm <- precip$DailyTotal_kgm2 * 0.01

# plot
w <-ggplot(data=precip, aes(x=date, y=DailyTotal_cm)) +
    geom_bar(stat="identity") +
    theme_bw()+
    labs(title = "", x = "", y = "Precipitation (cm)", color = "") +
    theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank())+
    scale_y_reverse() 
print(w)

dev.off()


# ------------------------------------------------------
# Compare to Precipitation
# plot everything together
pdf(paste(figs, "find_bug_kg_urban_with_precip.pdf", sep=""),width=11, height=8, onefile = T) 
for(i in 1:113){
  
  # read in data
  data <- read.csv(file=paste0('C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/output/bug_values_sub', i, '.csv', sep=''))
  data$dates <- seq(from=as.Date("2009-01-01"), to = as.Date("2017-12-31"), by = "day")
  
  # create a few new cols to analyze
  data$sub_develop_ha <- data$sub_area_ha*data$sub_perc_develop # hectares of developed land use in the subcatchment
  data$pur_app_for_sub_kg <- data$pur_app_kgha*data$sub_develop_ha # total kg that should be applied to the sub, based on its urban ha
  
  if (data$sub_perc_develop[1] == 0){
    data$pur_app_for_sub_kg <- rep(0, times=dim(data)[1])
  }
  
  # to use with plot title
  percent_develop <- round((data[1,12]*100), 2)
  
  # subset
  data <- data[, c("dates", "pur_app_for_sub_kg", "totl_bif_n_runf_kg")]
  
  # cumulative sum
  for (r in 2:dim(data)[1]){
    data[r,2] <- data[r-1,2] + data[r,2]
    data[r,3] <- data[r-1,3] + data[r,3]
  }
  
  # melt for plotting
  data_melt <- reshape2::melt(data, id.var='dates')
  head(data_melt)
  
  p <- ggplot(data_melt, aes(x=dates, y=value, col=variable)) + 
    geom_line() +
    xlab("")+
    ylab("Kilograms")+
    ggtitle(paste0("Cumulative Bifenthrin Applied to Urban Hectares for Subcatchment ", i, "(", percent_develop, "% developed)", sep=''))
  
  panel_plot <- cowplot::plot_grid(w,p, align = "h", nrow = 2, rel_heights = c(0.25, 0.75))
  panel_plot <- egg::ggarrange(w,p, heights = c(0.25, 0.75))
  print(panel_plot)
}
dev.off()


# ----------------------------------------------------------------------------
# Kilograms / Hectare (
pdf(paste(figs,"find_bug_kg_urban_all.pdf",sep=""),width=11,height=8)

# create a blank matrix
all_subs_pur <- data.frame(matrix(ncol = 1, nrow = dim(data)[1]))
all_subs_swmm <- data.frame(matrix(ncol = 1, nrow = dim(data)[1]))


for(i in 1:113){
  
  # read in data
  data <- read.csv(file=paste0('C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/output/bug_values_sub', i, '.csv', sep=''))
  
  # create a few new cols to analyze
  data$sub_develop_ha <- data$sub_area_ha*data$sub_perc_develop # hectares of developed land use in the subcatchment
  data$pur_app_for_sub_kg <- data$pur_app_kgha*data$sub_develop_ha # total kg that should be applied to the sub, based on its urban ha
  
  if (data$sub_perc_develop[1] == 0){
    data$pur_app_for_sub_kg <- rep(0, times=dim(data)[1])
  }
  
  all_subs_pur[,i+1] <- data$pur_app_for_sub_kg
  all_subs_swmm[,i+1] <- data$totl_bif_n_runf_kg

}  
all_subs_pur <- all_subs_pur[, -1]
all_subs_swmm <- all_subs_swmm[, -1]
all_subs_pur$pur_app_for_sub_totl_kg <- rowSums(all_subs_pur)
all_subs_swmm$totl_bif_n_runf_totl_kg <- rowSums(all_subs_swmm)

# subset data
all_subs <- data.frame(matrix(ncol = 1, nrow = dim(all_subs_pur)[1]))
all_subs$dates <- seq(from=as.Date("2009-01-01"), to = as.Date("2017-12-31"), by = "day")
all_subs$pur_app_for_sub_totl_kg <- all_subs_pur$pur_app_for_sub_totl_kg
all_subs$totl_bif_n_runf_totl_kg <- all_subs_swmm$totl_bif_n_runf_totl_kg
all_subs <- all_subs[, c("dates", "pur_app_for_sub_totl_kg", "totl_bif_n_runf_totl_kg")]

# cumulative sum
for (r in 2:dim(all_subs)[1]){
  all_subs[r,2] <- all_subs[r-1,2] + all_subs[r,2]
  all_subs[r,3] <- all_subs[r-1,3] + all_subs[r,3]
}
  
# melt to plot
data_melt <- reshape2::melt(all_subs, id.var='dates')
head(data_melt)
  
p <- ggplot(data_melt, aes(x=dates, y=value, col=variable)) + 
  geom_line() +
    
  xlab("")+
  ylab("Kilograms")+
  ggtitle("Cumulative Bifenthrin Applied to Urban Hectares for all Subcatchments")
  
print(p)
dev.off()


