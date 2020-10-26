# ---------------------------------------------------------------
# create *.txt file with 2192 app rates
# ---------------------------------------------------------------

source("path_names_ar.R")
library(dplyr)
filter = stats::filter

# ---------------------------------------------------------------
# set up the file for the 30-day moving average
# ---------------------------------------------------------------
# read in *.csv



placer <- read.csv(file=paste0(calpip_dir,"app_rates_09-17_pgc_inputs.csv"), header=TRUE) #JMS 9/22/20

(ar_io <- data.frame(day = unlist(sapply(placer$days,seq)),
                    month = rep(placer$month, times = placer$days),
                    year = rep(placer$year, times = placer$days),
                    value = rep(placer$bif_kgha_pgc/placer$days, times = placer$days))) %>% 
  write.table(paste0(calpip_dir,"app_rate_oi_for_swmm.txt"), 
              sep = "\t", row.names = F, col.names = F)

# # check/name variables
# nrow(placer)
# days <- placer$days
# 
# 
# # create output text file containing each day's app rate
# sink(file=paste0(calpip_dir,"app_rate_oi_for_swmm.txt"), append=TRUE) #JMS 9/22/20
# 
# 
# # for every day in each month, write a line regarding the application rate variables for SWMM .inp
# 
# for (i in 1:nrow(placer)){
#   # call variables
#   mm <- (placer[i,1])
#   yy <- placer[i,2]
#   value <- ((placer[i,5])/(placer[i,3]))
# 
#   
#   for (j in 1:days[i]){
#     # call variables
#     dd <- j
#     
#     # write line to file
#     cat(paste(dd,mm,yy,value,"\n", sep="\t"))
#     
#   }
# }
# sink()
# 


# --------------------------------------------------------
# apply a 30-day moving average
# --------------------------------------------------------

ar_io2 <- ar_io

ar_io2[-(1:31),] <- ar_io2[-(1:31),] %>% 
  mutate(value = as.vector(
    filter(x = ts(ar_io[,"value"]), filter = rep(1/30,30), 
           method = "convolution", sides = 1)
  )[-(1:31)])

write.table(ar_io2, paste0(calpip_dir,"app_rate_oi2_for_swmm.txt"), 
            sep = "\t", row.names = F, col.names = F)

# # read file back in to apply a 30-day moving average
# ma_placer <- read.table(file=paste0(calpip_dir,"app_rate_oi_for_swmm.txt")) #JMS 9/22/20
# con_ma_placer <- file(paste0(calpip_dir,"app_rate_oi_for_swmm.txt")) #JMS 9/22/20
# 
# a_old=readLines(con_ma_placer)
# a=readLines(con_ma_placer)
# close(con_ma_placer)
# 
# 
# # create vector of all app rates
# app_vec <- vector() 
# 
# for(i in 1:nrow(ma_placer)){
#   day_list <- unlist(strsplit(a[i], "\t")) #split up that day's list of var
#   app_vec[i] <- day_list[4] #insert that day's app into vec
# } 
# 
# 
# ma_vec <- vector()
# app_vec <- as.numeric(app_vec)
# 
# # jan 2009 moving average
# for(j in 1:31){
#   ma_vec[j] <- app_vec[j]
# }
# 
# # feb 2009 - end 30-day moving average
# # Use the "filter()" funtion for time series to calculate moving average
# ma_vec[32:length(app_vec)] <- as.vector(
#   filter(x=ts(app_vec),filter = rep(1/30,30), method = "convolution", sides = 1)
#   )[-(1:31)] #JMS 9/22/20
# 
# # make it characters, not numerics #JMS 9/22/20
# ma_vec <- as.character(ma_vec)
# 
# 
# # insert the app rates back into the file
# #???? This just reads what's already in it. It doesn't insert anything new #JMS 9/22/20
# con2_ma_placer <- file(paste0(calpip_dir,"app_rate_oi_for_swmm.txt")) #JMS 9/22/20
# 
# b_old=readLines(con2_ma_placer)
# b=readLines(con2_ma_placer)
# close(con2_ma_placer)
# 
# for(l in 1:length(ma_vec)){
#   day_list2 <- unlist(strsplit(b[l], "\t")) #split up that day's list of var
#   day_list2[4] <- ma_vec[l]
#   b[l]=paste(day_list2,collapse="\t")
# } 
# 
# 
# # write out file
# out_file <- paste(paste0(calpip_dir,"app_rate_oi2_for_swmm"),".txt", sep="") #JMS 9/22/20
# file.exists(out_file)
# file.create(out_file) # why did we check if we are just going to create it no matter what? #JMS 9/22/20
# file.exists(out_file)
# con_apps <- file(out_file)
# writeLines(b, con_apps)
# close(con_apps)


# --------------------------------------------------------
# reformat file for swmm
# --------------------------------------------------------

ar_io2 %>% 
  mutate(date = (seq(as.Date("2009-01-01"), as.Date("2017-12-31"), by="days") %>%
                   format("%m/%d/%Y")),
         time = rep("08:00", times=3287)) %>% 
  select("date", "time", "value") %>% 
  write.table(file=paste0(calpip_dir,"app_rate_output_for_swmm.txt"),
              sep="\t", row.names=F, col.names=F, quote=F)

# # read file 
# read_oi2 <- read.table(file=paste0(calpip_dir,"app_rate_oi2_for_swmm.txt")) #JMS 9/22/20
# 
# # columns should be:  date  time  value
# to_format <- read_oi2
# names(to_format) <- c("day", "month", "year", "value")
# to_format$date <- seq(as.Date("2009-01-01"), as.Date("2017-12-31"), by="days") #format 1961-01-01
# to_format$date <- format(to_format$date, format="%m/%d/%Y")
# to_format$time <- rep("08:00", times=3287)
# 
# to_output <- to_format[, c("date", "time", "value")]
# 
# write.table(to_output, file=paste0(calpip_dir,"app_rate_output_for_swmm.txt"),
#            sep="\t", row.names=F, col.names=F, quote=F) #JMS 9/22/20


# now, manually go into .txt to add headers and any desired comments, in swmm-readable format. consult swmm user manual.

# ---------------------------------------------------------------
# the end
# ---------------------------------------------------------------