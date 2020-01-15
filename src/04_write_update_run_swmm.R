# ---------------------------------------------------------------
# Run simulations: update swmm files with LHS parameter values 
# ---------------------------------------------------------------


# ---------------------------------------------------------------
# Create blank data frame for storage
# ---------------------------------------------------------------
myrun <- data.frame(date = seq(as.Date(simstart, format="%m/%d/%Y"),as.Date(simend, format="%m/%d/%Y"), by = "day"))
# ncols <- as.Date(as.character(simend), format="%m/%d/%Y")-
#   as.Date(as.character(simstart), format="%m/%d/%Y")


# Create empty dataframe for outputs
#############PRZM###########################################
# df_przm <- read.table(paste(pwcdir,"output/output",".zts", sep=""), header= FALSE, sep= "",
#                       skip = 3, stringsAsFactors = FALSE, row.names=NULL)
# # dim(df)
# str(df)
nrows_ro <- dim(myrun)[[1]]
ncols_ro <- 2
outputdf <- array(data=NA, c(nrows_ro,ncols_ro,Nsims))
dim(outputdf)


# ---------------------------------------------------------------
# For each simulation: update input file, run swmm, read outputs
# ---------------------------------------------------------------
set.seed(42)

for (Ite in 1:Nsims){
  print(Ite)
  con_swmm5 <- file(paste(swmmdir, "input/NPlesantCreek",".inp",sep=""))
  a_old=readLines(con_swmm5)
  a=readLines(con_swmm5)
  close(con_swmm5)
  
  
  newdir <- paste0(swmmdir,"input/input",Ite)
  print(newdir)
  dir.create(newdir,showWarnings = FALSE) 
  cwd <- getwd()          # CURRENT dir
  setwd(newdir) 

  # ---------------------------------------------------------------
  # parameter = NImperv
  # ---------------------------------------------------------------
  Num=113 # number of applications
  NImperv=round(input_list[Ite,"NImperv"],2)
  row_0=176
  for (i in 1:Num){
    row_t=row_0+(i-1)
    NImperv_list <- unlist(strsplit(a[row_t],"\\s+"))
    #cn_list[6]<-(as.numeric(CNPer[Ite]))*(as.numeric(cn_list[6]))
    NImperv_list[2]<-NImperv
    a[row_t]=paste(NImperv_list,collapse=" ")
    
  }
  
  # ---------------------------------------------------------------
  # parameter = NPerv
  # ---------------------------------------------------------------  
  Num=113 # number of applications
  NPerv=round(input_list[Ite,"NPerv"],2)
  row_0=176
  for (i in 1:Num){
    row_t=row_0+(i-1)
    NPerv_list <- unlist(strsplit(a[row_t],"\\s+"))
    #cn_list[6]<-(as.numeric(CNPer[Ite]))*(as.numeric(cn_list[6]))
    NPerv_list[3]<-NPerv
    a[row_t]=paste(NPerv_list,collapse=" ")
    
  }
  
  
  
  
  # ---------------------------------------------------------------
  # copy swmm.exe
  # ---------------------------------------------------------------
  print(paste(file.exists(swmmdir_executable), ": executable file at", swmmdir_executable))
  file.copy(swmmdir_executable,newdir, recursive = FALSE, 
            copy.mode = TRUE)
  
  # ---------------------------------------------------------------
  # copy swmm.dll
  # ---------------------------------------------------------------
  print(paste(file.exists(dlldir_executable), ": executable file at", dlldir_executable))
  file.copy(dlldir_executable,newdir, recursive = FALSE, 
            copy.mode = TRUE)
  
  # ---------------------------------------------------------------
  # write input (.inp) file
  # ---------------------------------------------------------------
  swmm_file <- paste("NPlesantCreek",".inp", sep="")
  file.exists(swmm_file)
  file.create(swmm_file)
  file.exists(swmm_file)
  con_swmm <-file(swmm_file)
  writeLines(a,
             con_swmm)
  close(con_swmm)
  
  # ---------------------------------------------------------------
  # initiate the simulation, save output, report files
  # ---------------------------------------------------------------

  #system2(swmmdir_executable, "NPlesantCreek.inp", "NPlesantCreek.rpt", "NPlesantCreek.out")
  
  #files <- run_swmm("NPlesantCreek.inp")
  
  # ---------------------------------------------------------------
  # initiate the simulation, save rpt and out files as temporary files (to save computer space)
  # ---------------------------------------------------------------
  tmp_rpt_file <- tempfile()
  tmp_out_file <- tempfile()
  

  # ---------------------------------------------------------------
  # run swmm
  # ---------------------------------------------------------------
  swmm_files <- run_swmm(
    inp = "NPlesantCreek.inp",
    rpt = tmp_rpt_file,
    out = tmp_out_file
  )
  
  # ---------------------------------------------------------------
  # read swmm results
  # ---------------------------------------------------------------
  results <- data.frame(read_out(swmm_files$out, iType = 3, object_name = "18",vIndex = 4))
  
  # ---------------------------------------------------------------
  # make edits to results
  # ---------------------------------------------------------------
 
  # move index column to first column [duplicate]
  results <- cbind(DateTime = rownames(results), results)
  rownames(results) <- 1:nrow(results)
  results$DateTime<-as.Date(results$DateTime,"%Y-%m-%d %H:%M:%S")
  
  # summarize results by date
  results$Date <- as.Date(results$DateTime) 
  results$Time <- format(as.POSIXct(results$DateTime) ,format = "%H:%M:%S") 
  head(results)
  

  # ---------------------------------------------------------------
  # save results
  # ---------------------------------------------------------------
  # write.csv(results, file = paste(swmmdir, "io/results_test.csv", sep = ""))
  # DateTime<-seq(as.POSIXct(simstart, format="%m/%d/%Y"),
  #                                  as.POSIXct(simend, format="%m/%d/%Y"),
  #                                  by="hour")
  # write.csv(DateTime , file = paste(swmmdir, "io/date_time.csv", sep = ""))
  # colnames(results) <- c("total runoff")
  # rownames(results) <- results$DateTime
  
  # df <- read.table(paste(newdir,"/","output",".zts", sep=""), header= FALSE, sep= "",
  #                  skip = 3, stringsAsFactors = FALSE, row.names=NULL)
  
  
  dailyro<-aggregate(results["total_runoff"], by=results["Date"], sum)
  #print(dailyro)
  #print(dim(dailyro))
  outputdf[1:nrows_ro,1:ncols_ro,Ite] <- abind(dailyro[1:nrows_ro,1:ncols_ro])
  #print(outputdf)
  #print(dim(outputdf))
  setwd(cwd)
}


# ---------------------------------------------------------------
# the end
# ---------------------------------------------------------------