# --------------------------------------------------------
# weather file for PGC SWMM
# --------------------------------------------------------

# setup environment
library(stringr)
library(dplyr)
library(tidyr)
library(devtools)
library(lubridate)
library(gdata)


# specify location
mydir <- "C:/Users/echelsvi/git/chelsvig_urban_pesticides/probabilistic_python/weather/" 

# read in weather file
precip <- read.csv(paste0(mydir,"Precipitation_nldas.csv"))


# subset data (kg/m2 = mm)
precip <- precip[1:122736,]
precip$Hourly_Total_kgm2 <- as.numeric(levels(precip$Hourly_Total_kgm2))[precip$Hourly_Total_kgm2]


# set up dataframe: station year month day hour minute precip
swmm_precip <- matrix(data=NA, nrow=dim(precip)[1], ncol=7, 
                      dimnames = list(c(), c("station", "year", "month", "day", "hour", "minute", "precip_mm")))
swmm_precip <- as.data.frame(swmm_precip)

# fill cols with values
swmm_precip$year <- substring(precip$Date,1,4)
swmm_precip$month <- substring(precip$Date,6,7)
swmm_precip$day <- substring(precip$Date,9,10)
swmm_precip$hour <- substring(precip$Date,12,13)
swmm_precip$minute <- rep("00", dim(precip)[1])
swmm_precip$precip_mm <- precip$Hourly_Total_kgm2
swmm_precip$station <- rep("swmm_wet", dim(precip)[1])

# write out
write.table(swmm_precip, file=paste0(mydir, "swmm_wet.txt", sep=""), quote=F, sep="\t",
            row.names=F, col.names=T)


# --------------------------------------------------------
# the end
# --------------------------------------------------------