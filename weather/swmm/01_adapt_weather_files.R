# --------------------------------------------------------
# adapt City of Roseville weather files to swmm-readable
# --------------------------------------------------------

library(stringr)
library(dplyr)
library(tidyr)

# specify location
mydir <- "C:/Users/echelsvi/git/chelsvig_urban_pesticides/weather/swmm/"

# read in the files
before_1572 <- read.csv(paste0(mydir, "1572.csv", sep=""), skip=2, header=F)
before_1601 <- read.csv(paste0(mydir, "1601.csv", sep=""), skip=2, header=F)
before_1602 <- read.csv(paste0(mydir, "1602.csv", sep=""), skip=2, header=F)
before_1783 <- read.csv(paste0(mydir, "1783.csv", sep=""), skip=2, header=F)


# ----------------------------------
# station 1572
# ----------------------------------

# split the date/time cols
before2_1572 <- before_1572 %>%
  separate(V1, c("date", "time"), " ")

before3_1572 <- before2_1572 %>%
  separate(date, c("month", "day", "year"), "/") %>%
  separate(time, c("hour", "minute"), ":")


# create/edit other cols
before3_1572$station <- rep("p1572", time=dim(before3_1572)[[1]])
before3_1572$minute <- rep(0, time=dim(before3_1572)[[1]])
names(before3_1572)[names(before3_1572) == "V2"] <- "precipitation"
before3_1572$precipitation <- before3_1572$precipitation*25.4 #in to mm
before3_1572[is.na(before3_1572)] <- 0


# final output (ordered as follows: station yyyy m d hour minute precip)
after_1572 <- before3_1572[,c("station", "year", "month", "day", "hour", "minute", "precipitation")]

# write out in tab-delimited
write.table(after_1572, file = paste0(mydir, "1572_out.txt",sep=""), sep="\t",row.names=F,col.names=T,quote=F)

#now manually append this file to the existing



# ----------------------------------
# station 1601
# ----------------------------------

# split the date/time cols
before2_1601 <- before_1601 %>%
  separate(V1, c("date", "time"), " ")

before3_1601 <- before2_1601 %>%
  separate(date, c("month", "day", "year"), "/") %>%
  separate(time, c("hour", "minute"), ":")


# create/edit other cols
before3_1601$station <- rep("P1601", time=dim(before3_1601)[[1]])
before3_1601$minute <- rep(0, time=dim(before3_1601)[[1]])
names(before3_1601)[names(before3_1601) == "V2"] <- "precipitation"
before3_1601$precipitation <- before3_1601$precipitation*25.4
before3_1601[is.na(before3_1601)] <- 0


# final output (ordered as follows: station yyyy m d hour minute precip)
after_1601 <- before3_1601[,c("station", "year", "month", "day", "hour", "minute", "precipitation")]

# write out in tab-delimited
write.table(after_1601, file = paste0(mydir, "1601_out.txt",sep=""), sep="\t",row.names=F,col.names=T,quote=F)

#now manually append this file to the existing


# ----------------------------------
# station 1602
# ----------------------------------

# split the date/time cols
before2_1602 <- before_1602 %>%
  separate(V1, c("date", "time"), " ")

before3_1602 <- before2_1602 %>%
  separate(date, c("month", "day", "year"), "/") %>%
  separate(time, c("hour", "minute"), ":")


# create/edit other cols
before3_1602$station <- rep("P1602", time=dim(before3_1602)[[1]])
before3_1602$minute <- rep(0, time=dim(before3_1602)[[1]])
names(before3_1602)[names(before3_1602) == "V2"] <- "precipitation"
before3_1602$precipitation <- before3_1602$precipitation*25.4
before3_1602[is.na(before3_1602)] <- 0


# final output (ordered as follows: station yyyy m d hour minute precip)
after_1602 <- before3_1602[,c("station", "year", "month", "day", "hour", "minute", "precipitation")]

# write out in tab-delimited
write.table(after_1602, file = paste0(mydir, "1602_out.txt",sep=""), sep="\t",row.names=F,col.names=T,quote=F)

#now manually append this file to the existing


# ----------------------------------
# station 1783
# ----------------------------------

# split the date/time cols
before2_1783 <- before_1783 %>%
  separate(V1, c("date", "time"), " ")

before3_1783 <- before2_1783 %>%
  separate(date, c("month", "day", "year"), "/") %>%
  separate(time, c("hour", "minute"), ":")


# create/edit other cols
before3_1783$station <- rep("STA01", time=dim(before3_1783)[[1]])
before3_1783$minute <- rep(0, time=dim(before3_1783)[[1]])
names(before3_1783)[names(before3_1783) == "V2"] <- "precipitation"
before3_1783$precipitation <- before3_1783$precipitation*25.4
before3_1783[is.na(before3_1783)] <- 0


# final output (ordered as follows: station yyyy m d hour minute precip)
after_1783 <- before3_1783[,c("station", "year", "month", "day", "hour", "minute", "precipitation")]

# write out in tab-delimited
write.table(after_1783, file = paste0(mydir, "1783_out.txt", sep=""), sep="\t",row.names=F,col.names=T,quote=F)

#now manually append this file to the existing



# --------------------------------------------------------
# the end
# --------------------------------------------------------