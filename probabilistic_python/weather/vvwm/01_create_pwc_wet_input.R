# --------------------------------------------------------
# adapt City of Roseville weather files to PWC-file-generator format
# --------------------------------------------------------

# setup environment
library(stringr)
library(dplyr)
library(tidyr)
library(devtools)
library(lubridate)
library(gdata)


# specify location
mydir <- "C:/Users/echelsvi/git/chelsvig_urban_pesticides/probabilistic_python/weather/vvwm/"

# read in the precip files
df_1572 <- read.table(paste0(mydir,"sp1572.dat"), header=T, sep="\t")
df_1601 <- read.table(paste0(mydir,"sp1601.dat"), header=T, sep="\t")
df_1602 <- read.table(paste0(mydir,"sp1602.dat"), header=T, sep="\t")
df_1783 <- read.table(paste0(mydir,"spp1783.dat"), header=T, sep="\t")

# read in other weather files
rad <- read.csv(paste0(mydir, "DWRadiation_nldas.csv"))
temp <- read.csv(paste0(mydir, "Temperature_nldas.csv"))
wind <- read.csv(paste0(mydir, "Wind_nldas.csv"))
evap <- read.csv(paste0(mydir, "Evapotranspiration_hargreaves.csv"))

# source function
source("00_function_pwcfg.R")


# ----------------------------------
# HMS data cleaning
# ----------------------------------

# evap ( ??  -> cm/day)
evap <- evap[1:3287, ]

# temp (Kelvin -> Celsius 
temp <- temp[1:3287, ]
temp$temp_c <- temp$Average.Temperature - 273.15

# solar radiation (W/m^2 -> Langley)
rad <- rad[1:3287, ]
rad$longwave <- as.numeric(levels(rad$longwave))[rad$longwave]
rad$rad_langley <- rad$longwave * .484583

# wind (U-wind and V-wind m/s -> Vector wind cm/s)
wind <- wind[1:3287, ]
wind$v <- as.numeric(levels(wind$v))[wind$v]
wind$wind_vector <- 100*(sqrt((wind$u)^2 + (wind$v)^2))


# ----------------------------------
# precip cleaning, final merge
# ----------------------------------

wet_files <- list(df_1572, df_1601, df_1602, df_1783)


for (wet in wet_files){
  
  # merge date cols
  wet$date <- as.Date(with(wet, paste(year, month, day, sep="-")), "%Y-%m-%d")
  
  
  # use dplyr and mutate to add a day column to your data
  daily_sum_precip <- wet %>%
    mutate(day = as.Date(date, format = "%Y-%m-%d"))%>%
    group_by(day) %>% # group by the day column
    summarise(precip_cm=sum(precipitation)) %>%  # calculate the SUM of all precipitation that occurred on each day
    na.omit()
  
  # edit cols
  daily_sum_precip$precip_cm <- daily_sum_precip$precip_cm*2.54 #inch to cm
  
  # subset
  daily_sum_precip <- daily_sum_precip[1828:5114, ]
  
  # append other weather vars
  full_weather <- daily_sum_precip
  full_weather$evap <- evap$Potential.Evapotranspiration
  full_weather$temp <- temp$temp_c
  full_weather$wind <- wind$wind_vector
  full_weather$solrad <- rad$rad_langley
  full_weather <- as.data.frame(full_weather)
  

  # PWC File Generator function (with modifications, due to errors)
  
  # variable set-up
  file <- full_weather
  
  names(file)[names(file) == "day"] <- "date"
  names(file)[names(file) == "precip_cm"] <- "precip_cm"
  names(file)[names(file) == "evap"] <- "pevp_cm"
  names(file)[names(file) == "temp"] <- "temp_celsius"
  names(file)[names(file) == "wind"] <- "ws10_cm_s"
  names(file)[names(file) == "solrad"] <- "solr_lang"
  
  format_date = "%Y-%m-%d" #maybe need to change format to format_date in the function ???
  start ="2009-01-01"
  end = "2017-12-31"
  save_in = paste0(mydir, "weather_", str_trim(wet$station[1]))
  
  
  # subset period
  file_PWC <- file[as.Date(file[ ,"date"], format = format_date) >= as.Date(start, format = format_date) & as.Date(file[ ,"date"], format = format_date) <= as.Date(end, format = format_date),]
  
  # Split dates into month, day and year
  split_dates <- as.character(format(as.Date(file_PWC[ ,"date"], format = format_date), "%m-%d-%y"))
  split_dates  <- strsplit(split_dates, "-")
  split_dates <- matrix(unlist(split_dates), ncol = 3, byrow = TRUE)
  
  # Weather file
  file_PWC_dates <- data.frame(split_dates,
                               precip_cm = file_PWC[, "precip_cm"],
                               pevp_cm = file_PWC[, "pevp_cm"],
                               temp_celsius = file_PWC[, "temp_celsius"],
                               ws10_cm_s = file_PWC[, "ws10_cm_s"],
                               solr_lang = file_PWC[, "solr_lang"])
  
  file_PWC_dates$empty <- NA
  file_PWC_dates <- file_PWC_dates[c("empty","X1", "X2","X3", "precip_cm", "pevp_cm",
                                     "temp_celsius", "ws10_cm_s", "solr_lang" )]

  
  file_PWC_dates$X3 <- year(seq(as.Date(start), by = "day",length.out = nrow(file_PWC_dates))) #needed to insert "start" in place of "61/01/01"
  
  # "Parana" gaps will be filled by the average value
  file_PWC_dates$precip_cm[is.na(file_PWC_dates$precip_cm)] <- 0
  file_PWC_dates$pevp_cm[is.na(file_PWC_dates$pevp_cm)] <- mean(file_PWC_dates$pevp_cm, na.rm = TRUE)
  file_PWC_dates$temp_celsius[is.na(file_PWC_dates$temp_celsius)] <- mean(file_PWC_dates$temp_celsius, na.rm = TRUE)
  file_PWC_dates$ws10_cm_s[is.na(file_PWC_dates$ws10_cm_s)] <- mean(file_PWC_dates$ws10_cm_s, na.rm = TRUE)
  file_PWC_dates$solr_lang[is.na(file_PWC_dates$solr_lang)] <- mean(file_PWC_dates$solr_lang, na.rm = TRUE)
  
  # Round numbers
  file_PWC_dates$precip_cm <- round(file_PWC_dates$precip_cm, digit = 2)
  file_PWC_dates$pevp_cm <- round(file_PWC_dates$pevp_cm, digit = 2)
  file_PWC_dates$temp_celsius <- round(file_PWC_dates$temp_celsius, digit = 1)
  file_PWC_dates$ws10_cm_s <- round(file_PWC_dates$ws10_cm_s, digit = 1)
  file_PWC_dates$solr_lang <- round(file_PWC_dates$solr_lang, digit = 1)
  
  # FORTRAN format 1X,3I2,5F10.0
  file_PWC_dates$X1 <- as.integer(as.character(file_PWC_dates$X1))
  file_PWC_dates$X2 <- as.integer(as.character(file_PWC_dates$X2))
  file_PWC_dates$X3 <- as.integer(as.character(file_PWC_dates$X3))
  
  file_PWC_dates$X1 <- sprintf("%02d", file_PWC_dates$X1) #leading zeros
  file_PWC_dates$X2 <- sprintf("%02d", file_PWC_dates$X2) 
  file_PWC_dates$X3 <- sprintf('%02d', file_PWC_dates$X3 %% 100) #ADDED THIS
  
  file_PWC_dates$precip_cm <- as.numeric(file_PWC_dates$precip_cm)
  file_PWC_dates$pevp_cm <- as.numeric(file_PWC_dates$pevp_cm)
  file_PWC_dates$temp_celsius <- as.numeric(file_PWC_dates$temp_celsius)
  file_PWC_dates$ws10_cm_s <- as.numeric(file_PWC_dates$ws10_cm_s)
  file_PWC_dates$solr_lang <- as.numeric(file_PWC_dates$solr_lang)
  
  #save file as .dvf in FORTRAN file format
  write.fwf(file_PWC_dates, file = paste(as.character(save_in), ".dvf", sep = ""),
            width = c(1, 2, 2, 2, 10, 10, 10, 10, 10),
            sep ="",
            colnames = FALSE)  
  
  
}




# --------------------------------------------------------
# the end
# --------------------------------------------------------