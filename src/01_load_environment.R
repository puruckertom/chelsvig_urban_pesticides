# -----------------------------------------------------------------------
# set-up environment
# -----------------------------------------------------------------------


# check to make sure required packages are installed
list.of.packages <- c("plyr", "dplyr", "reshape2", "ggplot2", "grid", "gridExtra", "sensitivity", "abind", 
                      "ppcor","swmmr", "DEoptim", "stringi", "purrr", "vctrs", "sf")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)>0) {install.packages(new.packages)}

install.packages("swmmr")

# install and load library dependencies
library(magrittr)
library(plyr)
library(reshape2)
library(ggplot2)
library(grid)
library(lhs)
library(gridExtra)
library(sensitivity)
library(abind)
library(tools)
library(ppcor)
library(dplyr)
library(swmmr)
library(DEoptim) #Differential Evolution algorithm in R
library(stringi)
library(purrr)
library(vctrs)
library(sf)
library(dplyr)

# echo environment
Sys.info()
Sys.info()[4]
.Platform
version


# set some default directories based on machine location
#Tom's epa window
if(Sys.info()[4]=="DZ2626UTPURUCKE"){
  pwcdir <- "d:/git/chelsvig_urban_pesticides/"
  # pwc,przm (without directory, the file needs to be in vpdir_exe above)
    swmm_filename <- "NPlesantCreek.inp"
}
#Sumathy's window
if(Sys.info()[4]=="DZ2626USSINNATH"){
  swmmdir <- "C:/git/chelsvig_urban_pesticides/"
  # pwc,przm file (without directory, the file needs to be in vpdir_exe above)
  swmm_filename <- "NPlesantCreek.inp"
}
#Sumathy's desktop
if(Sys.info()[4]=="DESKTOP-7UFGA86"){
  swmmdir <- "C:/Users/Sumathy/chelsvig_urban_pesticides/"
  # pwc,przm file (without directory, the file needs to be in vpdir_exe above)
  swmm_filename <- "NPlesantCreek.inp"
}
#Emma's epa 
if(Sys.info()[4]=="LZ2626UECHELSVI"){
  swmmdir <- "C:/Users/echelsvi/git/chelsvig_urban_pesticides/"
  # pwc,przm file (without directory, the file needs to be in vpdir_exe above)
  swmm_filename <- "NPlesantCreek.inp"
}
print(paste("Root directory location: ", swmmdir, sep=""))


# subdirectories
swmmdir_input <- paste(swmmdir, "input/", sep = "")
swmmdir_output <- paste(swmmdir, "output/", sep = "")
swmmdir_log <- paste(swmmdir, "log/", sep = "")
swmmdir_fig <- paste(swmmdir, "figures/", sep = "")
swmmdir_exe <- paste(swmmdir, "exe/", sep = "")
swmmdir_io <- paste(swmmdir, "io/", sep = "")
swmmdir_weather <- paste(swmmdir, "weather/", sep = "")
swmmdir_sobol <- paste(swmmdir, "sobol/", sep = "")


# swmm executable version (swmm 5)
swmm_binary<- "swmm5.exe"
swmmdir_executable <- paste(swmmdir_exe, swmm_binary, sep="")
dll_binary<- "swmm5.dll"
dlldir_executable <- paste(swmmdir_exe, dll_binary, sep="")


# -----------------------------------------------------------------------
# the end
# -----------------------------------------------------------------------