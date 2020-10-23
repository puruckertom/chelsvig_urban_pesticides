# ------------------------------------------------------------------------------
# compute monthly bifenthrin application rates (kg) for our placer county
# ------------------------------------------------------------------------------

source("path_names_ar.R")
library(dplyr)
# ------------------------------------------------------------------------------
# placer county
# ------------------------------------------------------------------------------

# filelist = list of all of the CALPIP data
filelist <- list.files(path=calpip_dir, pattern="^placer_\\d{4}.csv", full.names=TRUE) #JMS 9/22/20

# monthlist (1-12)
monthlist <- c("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")

combined_yearsums <- data.frame(month = c(), year = c(), bif_kg = c())

for (myfile in filelist){
  this_year <- substr(myfile, nchar(myfile)-7, nchar(myfile)-4) #JMS 9/22/20
  #read in file
  this_data <- read.csv(file=myfile, header=TRUE,sep=",")
  #format date
  this_data$DATE <- as.Date(this_data$DATE, format="%m/%d/%Y")
  
  #create blank dataframe for output of monthly sums
  # year_output <- data.frame(month = rep(NA, times = 12), 
  #                           year = rep(NA, times = 12), 
  #                           bif_kg = rep(NA, times = 12))
  
  # for (month in monthlist){
  #   # compute conversion from lb to kg, and kg/ha
  #   subset01 <- subset(this_data, format.Date(DATE, "%m")== month) #6 repeat rows??
  #   month_sum_lbs <- sum(subset01$POUNDS_CHEMICAL_APPLIED)
  #   month_sum_kg <- month_sum_lbs*0.453592 # conversion rate (pounds to kilograms)
  #   
  #   # fill in blank df
  #   row_pointer <- as.numeric(month)
  #   year_output[row_pointer,3] <- month_sum_kg
  #   year_output[row_pointer,2] <- this_year
  #   year_output[row_pointer,1] <- row_pointer
  # }
  year_output <- this_data %>% mutate(month = format.Date(DATE, "%m")) %>% 
    select(month, year = YEAR, POUNDS_CHEMICAL_APPLIED) %>% 
    group_by(month, year) %>% summarise(bif_kg = sum(POUNDS_CHEMICAL_APPLIED)) %>% 
    as.data.frame()
  
  # add to full period monthly sum table
  combined_yearsums <- combined_yearsums %>% rbind(year_output)

  file_part1 <- substr(myfile, 1, nchar(myfile)-4) #JMS 9/22/20
  write.csv(year_output, file=paste0(file_part1, "_month.csv"), row.names=F)
}

# # filelist = list of all of the year's monthly sums
# filelist02 <- list.files(path=calpip_dir, pattern="*_month.csv", full.names=TRUE) #JMS 9/22/20
# 
# # combine all years
# combined_yearsums <- do.call('rbind', lapply(filelist02, read.csv, header=TRUE))

# write out file
write.csv(combined_yearsums, file=paste0(calpip_dir,"placer_09-17.csv"), row.names=F) #JMS 9/22/20



# ------------------------------------------------------------------------------
# the end
# ------------------------------------------------------------------------------