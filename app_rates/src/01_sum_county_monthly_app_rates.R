# ------------------------------------------------------------------------------
# compute monthly bifenthrin application rates (kg) for our placer county
# ------------------------------------------------------------------------------

mypath = "C:/Users/Julia Stelman/Desktop/Watershed/chelsvig_urban_pesticides/app_rates/calpip/" #JMS 9/22/20

# ------------------------------------------------------------------------------
# placer county
# ------------------------------------------------------------------------------

# filelist = list of all of the CALPIP data
filelist <- list.files(path=mypath, pattern="^\\w*.csv", full.names=TRUE) #JMS 9/22/20

# monthlist (1-12)
monthlist <- c("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")


for (myfile in filelist){
  this_year <- substr(myfile, nchar(myfile)-7, nchar(myfile)-4) #JMS 9/22/20
  
  #read in file
  this_data <- read.csv(file=myfile, header=TRUE,sep=",")
  
  #format date
  this_data$DATE <- as.Date(this_data$DATE, format="%m/%d/%Y")
  
  #create blank matrix for output of monthly sums
  year_output <- matrix(data=NA, nrow=12, ncol=3)
  year_output <- as.data.frame(year_output)
  colnames(year_output) <- c("month", "year", "bif_kg")
  
  for (month in monthlist){
    # compute conversion from lb to kg, and kg/ha
    subset01 <- subset(this_data, format.Date(DATE, "%m")== month)
    month_sum_lbs <- sum(subset01$POUNDS_CHEMICAL_APPLIED)
    month_sum_kg <- month_sum_lbs*0.453592 # conversion rate (pounds to kilograms)
    
    # fill in blank df
    row_pointer <- as.numeric(month)
    year_output[row_pointer,3] <- month_sum_kg
    year_output[row_pointer,2] <- this_year
    year_output[row_pointer,1] <- row_pointer
  }
  file_part1 <- substr(myfile, 1, nchar(myfile)-4) #JMS 9/22/20
  write.csv(year_output, file=paste0(file_part1, "_month.csv", sep=""), row.names=F)
}



# filelist = list of all of the year's monthly sums
filelist02 <- list.files(path=mypath, pattern="*_month.csv", full.names=TRUE) #JMS 9/22/20

# combine all years
combined_yearsums <- do.call('rbind', lapply(filelist02, read.csv, header=TRUE))

# write out file
write.csv(combined_yearsums, file=paste0(mypath,"placer_09-17.csv"), row.names=F) #JMS 9/22/20



# ------------------------------------------------------------------------------
# the end
# ------------------------------------------------------------------------------