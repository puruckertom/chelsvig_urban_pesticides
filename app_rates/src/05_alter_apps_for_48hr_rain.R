# ---------------------------------------------------------------
# alter applications to account for 48hr application rule
# ---------------------------------------------------------------
library(tidyr)

# set up
dir_weather <- "C:/Users/echelsvi/git/chelsvig_urban_pesticides/probabilistic_python/weather/"
dir_apps <- "C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/"

# read in apps and precip files
daily_apps <- read.table(paste0(dir_apps, "calpip/app_rate_output_for_swmm.txt", sep=''),skip = 3, header=F)
daily_apps$date <- seq(from=as.Date("2009-01-01"), to = as.Date("2017-12-31"), by = "day")
daily_apps$apps_kgha <- daily_apps$V3

daily_precip <- read.csv(file=paste0(dir_weather, "Precipitation_nldas_daily.csv", sep=""), header=TRUE, sep=",")
daily_precip <- daily_precip[1:3287, ]
daily_precip$date <- seq(as.Date("2009-01-01"), as.Date("2017-12-31"), by="days")
daily_precip$DailyTotal_kgm2 <- as.numeric(levels(daily_precip$DailyTotal_kgm2))[daily_precip$DailyTotal_kgm2]


# merge files
apps_precip <- daily_apps[, c(4:5)]
apps_precip$precip_mm <- daily_precip$DailyTotal_kgm2

# create yes/no rainfall column
apps_precip$rainbuff <- NA
apps_precip$apps_update_kgha <- apps_precip$apps_kgha



# reduce apps to 0 if rainfall within 48hr
for (d in 2:dim(apps_precip)[1]-1){
  
  # for all days (except first and last)
  # name the variables
  today_rain <- apps_precip[d,3]
  yester_rain <- apps_precip[d-1, 3]
  tomor_rain <- apps_precip[d+1, 3]
  today_buff <- apps_precip[d,4]
  
  # 1/0 based on rain within 48 hours
  if (today_rain != 0 || yester_rain != 0 || tomor_rain != 0){
    today_buff <- 1
  } else {
    today_buff <- 0
  }
  apps_precip[d,4] <- today_buff
  
  if (today_buff == 1){
    apps_precip[d,5] <- 0
  }
}


# for first day
d <- 1
# name the variables
today_rain <- apps_precip[d,3]
tomor_rain <- apps_precip[d+1, 3]
today_buff <- apps_precip[d,4]

# 1/0 based on rain within 48 hours
if (today_rain != 0 || tomor_rain != 0){
  today_buff <- 1
} else {
  today_buff <- 0
}
apps_precip[d,4] <- today_buff
if (apps_precip[d,4] == 1){
  apps_precip[d,5] <- 0
}
  
  
# for last day
d <- 3287
# name the variables
today_rain <- apps_precip[d,3]
yester_rain <- apps_precip[d-1, 3]
today_buff <- apps_precip[d,4]

# 1/0 based on rain within 48 hours
if (today_rain != 0 || yester_rain != 0){
  today_buff <- 1
} else {
  today_buff <- 0
}
apps_precip[d,4] <- today_buff
if (apps_precip[d,4] == 1){
  apps_precip[d,5] <- 0
}


# create a difference col
apps_precip$app_diff <- apps_precip$apps_kgha - apps_precip$apps_update_kgha


# re-incorporate the lost applications:
# separate date col into components
apps_precip <- apps_precip %>%
  separate(date, sep="-", into = c("year", "month", "day"))

# add another app update col
apps_precip$apps_update2_kgha <- NA

# set up loop vars
years <- c("2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017")
months <- c("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")


# loop through each year
for (y in years){
  # subset the year
  yr_subset <- apps_precip[which(apps_precip$year==y), ]
  
  # loop through each month
  for (m in months){
    # subset the month
    m_subset <- yr_subset[which(yr_subset$month==m), ]
    
    # count number of days that get apps
    app_days <- length(m_subset$rainbuff[m_subset$rainbuff == 0])
    
    # sum the lost apps
    app_lost <- sum(m_subset$app_diff)
    
    # divide by number of days that get apps, to divy up
    divy <- app_lost/app_days
    
    # add divy to each of the app days
    for (row in 1:nrow(m_subset)){
      if (m_subset[row,"rainbuff"] == 0){
        m_subset[row,"apps_update2_kgha"] = m_subset[row,"apps_update_kgha"] + divy
      } else{
        m_subset[row,"apps_update2_kgha"] = 0
      }
    }
    if (m == "01"){
      master_month <- data.frame(m_subset)
    } else{
      df <- data.frame(m_subset)
      master_month <- rbind(master_month,df) 
    }
  }
  if (y == "2009"){
    master_year <- master_month
  } else{
    master_year <- rbind(master_year, master_month)
  }
}

# create app rate output file for swmm
master_year$time <- rep('01:00', dim(master_year)[1])
master_year$date <- seq(from=as.Date("2009-01-01"), to = as.Date("2017-12-31"), by = "day")
out_file <- master_year[, c("date", "time", "apps_update2_kgha")]
out_file$date <- format(as.Date(out_file$date), "%m/%d/%Y")

# read out
write.table(out_file, paste0(dir_apps, "calpip/app_rate_output_for_swmm_48rain.txt", sep=""), quote=F, sep="\t", row.names=F, col.names=F)


# ----------------------------------------------------------------
# the end
# ----------------------------------------------------------------