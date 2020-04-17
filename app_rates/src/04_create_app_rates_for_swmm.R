# ---------------------------------------------------------------
# create *.txt file with 2192 app rates
# ---------------------------------------------------------------




# ---------------------------------------------------------------
# set up the file for the 30-day moving average
# ---------------------------------------------------------------
# read in *.csv
placer <- read.csv(file="C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/calpip/app_rates_09-17_pgc_inputs.csv", header=TRUE)

# check/name variables
nrow(placer)
days <- placer$days


# create output text file containing each day's app rate
sink(file="C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/calpip/app_rate_oi_for_swmm.txt", append=TRUE)


# for every day in each month, write a line regarding the application rate variables for SWMM .inp

for (i in 1:nrow(placer)){
  # call variables
  mm <- (placer[i,1])
  yy <- placer[i,2]
  value <- ((placer[i,5])/(placer[i,3]))

  
  for (j in 1:days[i]){
    # call variables
    dd <- j
    
    # write line to file
    cat(paste(dd,mm,yy,value,"\n", sep="\t"))
    
  }
}
sink()


# --------------------------------------------------------
# apply a 30-day moving average
# --------------------------------------------------------


# read file back in to apply a 30-day moving average
ma_placer <- read.table(file="C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/calpip/app_rate_oi_for_swmm.txt")
con_ma_placer <- file("C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/calpip/app_rate_oi_for_swmm.txt")

a_old=readLines(con_ma_placer)
a=readLines(con_ma_placer)
close(con_ma_placer)


# create vector of all app rates
app_vec <- vector() 

for(i in 1:nrow(ma_placer)){
  day_list <- unlist(strsplit(a[i], "\t")) #split up that day's list of var
  app_vec[i] <- day_list[4] #insert that day's app into vec
} 


ma_vec <- vector()
app_vec <- as.numeric(app_vec)

# jan 2009 moving average
for(j in 1:31){
  ma_vec[j] <- app_vec[j]
}

# feb 2009 - end 30-day moving average
for(k in 32:length(app_vec)){
  ma_vec[k] <- (app_vec[k-30]+app_vec[k-29]+app_vec[k-28]+app_vec[k-27]+app_vec[k-26]+app_vec[k-25]+app_vec[k-24]+app_vec[k-23]+app_vec[k-22]+
                  app_vec[k-21]+app_vec[k-20]+app_vec[k-19]+app_vec[k-18]+app_vec[k-17]+app_vec[k-16]+app_vec[k-15]+app_vec[k-14]+app_vec[k-13]+
    app_vec[k-12]+app_vec[k-11]+app_vec[k-10]+app_vec[k-9]+app_vec[k-8]+app_vec[k-7]+app_vec[k-6]+app_vec[k-5]+app_vec[k-4]+app_vec[k-3]+
    app_vec[k-2]+app_vec[k-1])/30
}

ma_vec <- as.character(ma_vec)


# insert the app rates back into the file
con2_ma_placer <- file("C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/calpip/app_rate_oi_for_swmm.txt")

b_old=readLines(con2_ma_placer)
b=readLines(con2_ma_placer)
close(con2_ma_placer)

for(l in 1:length(ma_vec)){
  day_list2 <- unlist(strsplit(b[l], "\t")) #split up that day's list of var
  day_list2[4] <- ma_vec[l]
  b[l]=paste(day_list2,collapse="\t")
} 


# write out file
out_file <- paste("C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/calpip/app_rate_oi2_for_swmm",".txt", sep="")
file.exists(out_file)
file.create(out_file)
file.exists(out_file)
con_apps <- file(out_file)
writeLines(b, con_apps)
close(con_apps)


# --------------------------------------------------------
# reformat file for swmm
# --------------------------------------------------------

# read file 
read_oi2 <- read.table(file="C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/calpip/app_rate_oi2_for_swmm.txt")

# columns should be:  date  time  value
to_format <- read_oi2
names(to_format) <- c("day", "month", "year", "value")
to_format$date <- seq(as.Date("2009-01-01"), as.Date("2017-12-31"), by="days") #format 1961-01-01
to_format$date <- format(to_format$date, format="%m/%d/%Y")
to_format$time <- rep("08:00", times=3287)

to_output <- to_format[, c("date", "time", "value")]

write.table(to_output, file="C:/Users/echelsvi/git/chelsvig_urban_pesticides/app_rates/calpip/app_rate_output_for_swmm.txt",
           sep="\t", row.names=F, col.names=F, quote=F)


# now, manually go into .txt to add headers and any desired comments, in swmm-readable format. consult swmm user manual.

# ---------------------------------------------------------------
# the end
# ---------------------------------------------------------------