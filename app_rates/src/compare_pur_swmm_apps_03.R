# ---------------------------------------------------------------
# visually examine swmm bifenthrin loadings
# ---------------------------------------------------------------

# setup
library(ggplot2)
library(gtable)
library(lubridate)
library(dplyr)

figs <- "C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/figures/"
dir_weather <- "C:/Users/echelsvi/git/chelsvig_urban_pesticides/probabilistic_python/weather/swmm/"


# ------------------------------------------------------
# Kilograms
pdf(paste(figs,"find_bug_kg_urban.pdf",sep=""),width=11,height=8, onefile=TRUE)


for(i in 1:113){

  # read in data
  data <- read.csv(file=paste0('C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/output/bug_values_sub', i, '.csv', sep=''))
  data$dates <- seq(from=as.Date("2009-01-02"), to = as.Date("2017-12-31"), by = "day")
  
  # create a few new cols to analyze
  data$sub_develop_ha <- data$sub_area_ha*data$sub_perc_develop # hectares of developed land use in the subcatchment
  data$pur_app_for_sub_kg <- data$pur_app_kgha*data$sub_develop_ha # total kg that should be applied to the sub, based on its urban ha
  
  if (data$sub_perc_develop[1] == 0){
    data$pur_app_for_sub_kg <- rep(0, times=dim(data)[1])
  }
  
  
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
    ggtitle(paste0("Cumulative Bifenthrin Applied to Urban Hectares for Subcatchment ", i, sep=''))

    
  print(p)
}
dev.off()


# # need to change...
# # add an if/then statement for all the precip files according to the subcatchment
# pdf(paste(figs,"find_bug_precip.pdf",sep=""),width=11,height=8, onefile=TRUE)
# 
# weather <- list("sp1572.dat", "sp1601.dat", "sp1602.dat", "spp1783.dat")
# 
# for (wet in weather){
#   # read in weather file
#   precip <- read.table(file=paste(dir_weather, wet, sep=""), header=TRUE, sep="\t")
#   precip <- precip[43848:122732, ]
# 
#   # create a date col
#   precip$MONTH <- sprintf("%02d", precip$month) # fix to 2 characters
#   precip$DAY <- sprintf("%02d", precip$day) # fix to 2 characters
#   
#   precip <- transform(precip,date=interaction(year,MONTH,DAY,sep='-'))
#   precip$date <- as.Date(precip$date)
#   
#   # calculate the daily precip 
#   num <- aggregate(precipitation~date,precip,length)
#   names(num)[2] <- 'num'
#   
#   totalp <- aggregate(precipitation~date,precip,sum)
#   names(totalp)[2] <- 'totalp'
#   
#   daily_precip <- merge(num,totalp)
#   
#   
#   # plot
#   w <-ggplot(data=daily_precip, aes(x=date, y=totalp)) +
#     geom_bar(stat="identity") +
#     ylab("Precipitation (cm)")+
#     ggtitle(paste0("Daily Precipitation, Site: ", substring(wet, 1, 7), sep=''))
#   print(w)
# 
# }
# dev.off()


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
all_subs$dates <- seq(from=as.Date("2009-01-02"), to = as.Date("2017-12-31"), by = "day")
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


