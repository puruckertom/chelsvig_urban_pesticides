# ---------------------------------------------------------------
# alter applications to account for 48hr application rule
# ---------------------------------------------------------------


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
  
  
# for first day
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



# create app rate output file for swmm
apps_precip$time <- rep('08:00', dim(apps_precip)[1])
out_file <- apps_precip[, c("date", "time", "apps_update_kgha")]
out_file$date <- format(as.Date(out_file$date), "%m/%d/%Y")

# read out
write.table(out_file, paste0(dir_apps, "calpip/app_rate_output_for_swmm_48rain.txt", sep=""), quote=F, sep="\t", row.names=F, col.names=F)


# ----------------------------------------------------------------
# the end
# ----------------------------------------------------------------