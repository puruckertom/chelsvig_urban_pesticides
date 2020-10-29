# ---------------------------------------------------------------
# visually examine swmm bifenthrin loadings
# ---------------------------------------------------------------

# setup
library(ggplot2)
# library(gtable)
# library(lubridate)
library(dplyr)

source("path_names_ar.R")

figs <- paste0(main_dir,"app_rates/figures/") #JMS 9/22/20
dir_weather <- paste0(main_dir,"probabilistic_python/weather/") #JMS 9/22/20


# -------------------------------------------------
# function for making cummulative sum plots
#--------------------------------------------------
make_cumsum_plot <- function(i){

  percent_develop1 <- 0
  
  p <- read.csv(file = paste0(main_dir,'app_rates/output/bug_values_sub', i, '.csv'),
                colClasses = c("Date",rep("numeric",11))) %>% 
    mutate(
      # hectares of developed land use in the subcatchment
      sub_develop_ha = sub_area_ha * sub_perc_develop,
      # total kg that should be applied to the sub, based on its urban ha
      pur_app_for_sub_kg = pur_app_kgha * sub_area_ha * sub_perc_develop) %>% 
    (function(df){ percent_develop1 <<- round((df[1,12]*100), 2)
    return(df) }) %>% select(dates, pur_app_for_sub_kg, totl_bif_n_runf_kg) %>% 
    mutate(pur_app_for_sub_kg = cumsum(pur_app_for_sub_kg),
           totl_bif_n_runf_kg = cumsum(totl_bif_n_runf_kg)) %>% 
    reshape2::melt(id.var='dates') %>% 
    ggplot(mapping = aes(x=dates, y=value, col=variable)) +
    geom_line() + xlab("")+ ylab("Kilograms")+
    ggtitle(paste0("Cummulative Bifenthrin Applied to Urban Hectares for Subcatchment ",
                   i, "(", percent_develop1, "% developed)")) 

  # # read in data
  # data <- read.csv(file=paste0(main_dir,'app_rates/output/bug_values_sub', i, '.csv')) #JMS 10/28/20
  # data$dates <- seq(from=as.Date("2009-01-01"), to = as.Date("2017-12-31"), by = "day")
  # 
  # # create a few new cols to analyze
  # data$sub_develop_ha <- data$sub_area_ha*data$sub_perc_develop # hectares of developed land use in the subcatchment
  # data$pur_app_for_sub_kg <- data$pur_app_kgha*data$sub_develop_ha # total kg that should be applied to the sub, based on its urban ha
  # 
  # if (data$sub_perc_develop[1] == 0){
  #   data$pur_app_for_sub_kg <- rep(0, times=dim(data)[1])
  # }
  # 
  # # to use with plot title
  # percent_develop <- round((data[1,12]*100), 2)
  # 
  # # subset
  # data <- data[, c("dates", "pur_app_for_sub_kg", "totl_bif_n_runf_kg")]
  # 
  # # cummulative sum
  # data$pur_app_for_sub_kg <- cumsum(data$pur_app_for_sub_kg) #JMS 9/23/20
  # data$totl_bif_n_runf_kg <- cumsum(data$totl_bif_n_runf_kg) #JMS 9/23/20
  # 
  # # melt for plotting
  # data_melt <- reshape2::melt(data, id.var='dates')
  # 
  # p <- ggplot(data_melt, aes(x=dates, y=value, col=variable)) + 
  #   geom_line() +
  #   xlab("")+
  #   ylab("Kilograms")+
  #   ggtitle(paste0("Cummulative Bifenthrin Applied to Urban Hectares for Subcatchment ", i, "(", percent_develop, "% developed)", sep=''))
  return(p)
}
# ------------------------------------------------------

# Make some plots for finding the over estimation bug

# Kilograms
pdf(paste(figs,"find_bug_kg_urban.pdf",sep=""),width=11,height=8, onefile=TRUE)

for(i in 1:113){
  print(make_cumsum_plot(i)) #(functionized) -JMS 9/23/20
}
dev.off()

# ------------------------------------------------------
# Precipitation

# read in weather file, make necessary edits and plot

w <- read.csv(file=paste0(dir_weather, "Precipitation_nldas_daily.csv"), 
              header=TRUE, sep=",", nrows = 3287, colClasses = c("Date","numeric")) %>% 
  mutate(DailyTotal_cm = DailyTotal_kgm2 * 0.01) %>% 
  ggplot(mapping = aes(x=Date, y=DailyTotal_cm)) +
  geom_bar(stat="identity") + theme_bw()+
  labs(title = "", x = "", y = "Precipitation (cm)", color = "") +
  theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank())+
  scale_y_reverse() 

# precip <- read.csv(file=paste0(dir_weather, "Precipitation_nldas_daily.csv", sep=""), header=TRUE, sep=",")
# precip <- precip[1:3287, ]
# precip$Date <- seq(as.Date("2009-01-01"), as.Date("2017-12-31"), by="days") #JMS 9/23/20
# precip$DailyTotal_kgm2 <- as.numeric(as.character(precip$DailyTotal_kgm2)) #JMS 9/23/20
# precip$DailyTotal_cm <- precip$DailyTotal_kgm2 * 0.01
# 
# # plot
# w <-ggplot(data=precip, aes(x=Date, y=DailyTotal_cm)) +
#     geom_bar(stat="identity") +
#     theme_bw()+
#     labs(title = "", x = "", y = "Precipitation (cm)", color = "") +
#     theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank())+
#     scale_y_reverse() 

# print to PDF -JMS 9/23/20
pdf(paste(figs,"find_bug_precip.pdf",sep=""),width=11,height=8) #(moved) -JMS 9/23/20
print(w)

dev.off()


# ------------------------------------------------------
# Compare to Precipitation
# plot everything together
pdf(paste(figs, "find_bug_kg_urban_with_precip.pdf", sep=""),width=11, height=8, onefile = T) 

for(i in 1:11){
  # make cummulative sum plot
  p <- make_cumsum_plot(i) #(functionized) -JMS 9/23/20
  
  panel_plot <- cowplot::plot_grid(w,p, align = "h", nrow = 2, rel_heights = c(0.25, 0.75))
  panel_plot <- egg::ggarrange(w,p, heights = c(0.25, 0.75))
  print(panel_plot)
}
dev.off()


# ----------------------------------------------------------------------------
# Kilograms / Hectare (
pdf(paste(figs,"find_bug_kg_urban_all.pdf",sep=""),width=11,height=8)

# new 10/28/20 { ------------------------------------

all_subs_pur <- data.frame(matrix(ncol = 1, nrow = 3287))
all_subs_swmm <- data.frame(matrix(ncol = 1, nrow = 3287))

for (i in 1:113){
  # read in datos
  datos <- read.csv(file=paste0(main_dir,'app_rates/output/bug_values_sub1.csv'),
                    colClasses = c("Date",rep("numeric",11))) %>% mutate(
                      # hectares of developed land use in the subcatchment
                      sub_develop_ha = sub_area_ha * sub_perc_develop,
                      # total kg that should be applied to the sub, based on its urban ha
                      pur_app_for_sub_kg = pur_app_kgha * sub_area_ha * sub_perc_develop) 
  
  all_subs_pur[,i] <- datos$pur_app_for_sub_kg
  all_subs_swmm[,i] <- datos$totl_bif_n_runf_kg
}

# ----------------------------------------- end new 10/28/20 JMS

# # create a blank matrix
# all_subs_pur <- data.frame(matrix(ncol = 1, nrow = dim(data)[1]))
# all_subs_swmm <- data.frame(matrix(ncol = 1, nrow = dim(data)[1]))
# 
# # now we are creating a giant data frame from all the data in all the files, adding the data file/col by file/col
# for(i in 1:113){
#   
#   # read in data
#   data <- read.csv(file=paste0(main_dir,'app_rates/output/bug_values_sub', i, '.csv')) #JMS 9/22/20
#   
#   # create a few new cols to analyze
#   data$sub_develop_ha <- data$sub_area_ha*data$sub_perc_develop # hectares of developed land use in the subcatchment
#   data$pur_app_for_sub_kg <- data$pur_app_kgha*data$sub_develop_ha # total kg that should be applied to the sub, based on its urban ha
#   
#   if (data$sub_perc_develop[1] == 0){
#     data$pur_app_for_sub_kg <- rep(0, times=dim(data)[1])
#   }
#   
#   all_subs_pur[,i+1] <- data$pur_app_for_sub_kg
#   all_subs_swmm[,i+1] <- data$totl_bif_n_runf_kg
# 
# }  

# make "total" columns
all_subs <- all_subs_pur %>% 
  transmute(dates = seq(from=as.Date("2009-01-01"), to = as.Date("2017-12-31"), by = "day"),
            pur_app_for_sub_totl_kg = cumsum(rowSums(all_subs_pur)),
            totl_bif_n_runf_totl_kg = cumsum(rowSums(all_subs_swmm)))

# # delete the original columns (not useful)
# all_subs_pur <- all_subs_pur[, -1]
# all_subs_swmm <- all_subs_swmm[, -1]
# 
# # make "total" columns
# all_subs_pur$pur_app_for_sub_totl_kg <- rowSums(all_subs_pur)
# all_subs_swmm$totl_bif_n_runf_totl_kg <- rowSums(all_subs_swmm)
# 
# # subset data
# all_subs <- data.frame(matrix(ncol = 1, nrow = dim(all_subs_pur)[1]))
# all_subs$dates <- seq(from=as.Date("2009-01-01"), to = as.Date("2017-12-31"), by = "day")
# all_subs$pur_app_for_sub_totl_kg <- all_subs_pur$pur_app_for_sub_totl_kg
# all_subs$totl_bif_n_runf_totl_kg <- all_subs_swmm$totl_bif_n_runf_totl_kg
# all_subs <- all_subs[, c("dates", "pur_app_for_sub_totl_kg", "totl_bif_n_runf_totl_kg")]
# 
# # cummulative sum -JMS 9/23/20
# all_subs$pur_app_for_sub_totl_kg <- cumsum(all_subs$pur_app_for_sub_totl_kg) #JMS 9/23/20
# all_subs$totl_bif_n_runf_totl_kg <- cumsum(all_subs$totl_bif_n_runf_totl_kg) #JMS 9/23/20

# melt to plot
data_melt <- reshape2::melt(all_subs, id.var='dates')

p <- ggplot(data_melt, aes(x=dates, y=value, col=variable)) + 
  geom_line() +
  xlab("")+
  ylab("Kilograms")+
  ggtitle("Cummulative Bifenthrin Applied to Urban Hectares for all Subcatchments")
  
print(p)
dev.off()


