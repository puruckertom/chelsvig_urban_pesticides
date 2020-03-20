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
  con_swmm5 <- file(paste(swmmdir, "input/swmm/NPlesantCreek",".inp",sep=""))
  a_old=readLines(con_swmm5)
  a=readLines(con_swmm5)
  close(con_swmm5)
  
  
  newdir <- paste0(swmmdir,"input/swmm/input",Ite)
  print(newdir)
  dir.create(newdir,showWarnings = FALSE) 
  cwd <- getwd()          # CURRENT dir
  setwd(newdir) 

  
  
  
  # ---------------------------------------------------------------
  # parameter = Kwidth
  # ---------------------------------------------------------------
  Num=113 # number of subcatchments
  Kwidth=round(input_list[Ite,"Kwidth"],2)
  row_0=59
  for (i in 1:Num){
    row_t=row_0+(i-1)
    Kwidth_list <- unlist(strsplit(a[row_t],"\\s+"))
    current_Kwidth <- as.numeric(Kwidth_list[6])
    Kwidth_list[6] <-round((Kwidth*current_Kwidth), 2)
    a[row_t]=paste(Kwidth_list,collapse=" ")
    
  }
  
  # ---------------------------------------------------------------
  # parameter = Kslope
  # ---------------------------------------------------------------
  Num=113 # number of subcatchments
  Kslope=round(input_list[Ite,"Kslope"],2)
  row_0=59
  for (i in 1:Num){
    row_t=row_0+(i-1)
    Kslope_list <- unlist(strsplit(a[row_t],"\\s+"))
    current_Kslope <- as.numeric(Kslope_list[7])
    Kslope_list[7] <-round((Kslope*current_Kslope), 2)
    a[row_t]=paste(Kslope_list,collapse=" ")
    
  }
  
  # ---------------------------------------------------------------
  # parameter = KImperv
  # ---------------------------------------------------------------
  Num=113 # number of subcatchments
  KImperv=round(input_list[Ite,"KImperv"],2)
  row_0=59
  for (i in 1:Num){
    row_t=row_0+(i-1)
    KImperv_list <- unlist(strsplit(a[row_t],"\\s+"))
    current_KImperv <- as.numeric(KImperv_list[5])
    KImperv_list[5] <-round((KImperv*current_KImperv), 2)
    a[row_t]=paste(KImperv_list,collapse=" ")
    
  }
  
  
  # ---------------------------------------------------------------
  # parameter = NImperv
  # ---------------------------------------------------------------
  Num=113 # number of subcatchment
  NImperv=round(input_list[Ite,"NImperv"],4)
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
  Num=113 # number of subcatchments
  NPerv=round(input_list[Ite,"NPerv"],3)
  row_0=176
  for (i in 1:Num){
    row_t=row_0+(i-1)
    NPerv_list <- unlist(strsplit(a[row_t],"\\s+"))
    NPerv_list[3]<-NPerv
    a[row_t]=paste(NPerv_list,collapse=" ")
    
  }
  
  
  # ---------------------------------------------------------------
  # parameter = SImperv
  # ---------------------------------------------------------------
  Num=113 # number of subcatchment
  SImperv=round(input_list[Ite,"SImperv"],2)
  row_0=176
  for (i in 1:Num){
    row_t=row_0+(i-1)
    SImperv_list <- unlist(strsplit(a[row_t],"\\s+"))
    SImperv_list[4]<-SImperv
    a[row_t]=paste(SImperv_list,collapse=" ")
    
  }
  
  # ---------------------------------------------------------------
  # parameter = SPerv
  # ---------------------------------------------------------------  
  Num=113 # number of subcatchments
  SPerv=round(input_list[Ite,"SPerv"],2)
  row_0=176
  for (i in 1:Num){
    row_t=row_0+(i-1)
    SPerv_list <- unlist(strsplit(a[row_t],"\\s+"))
    SPerv_list[5]<-SPerv
    a[row_t]=paste(SPerv_list,collapse=" ")
    
  }
  
  # ---------------------------------------------------------------
  # parameter = PctZero
  # ---------------------------------------------------------------  
  Num=113 # number of subcatchments
  PctZero=round(input_list[Ite,"PctZero"],2)
  row_0=176
  for (i in 1:Num){
    row_t=row_0+(i-1)
    PctZero_list <- unlist(strsplit(a[row_t],"\\s+"))
    PctZero_list[6]<-PctZero
    a[row_t]=paste(PctZero_list,collapse=" ")
    
  }
  
  # ---------------------------------------------------------------
  # parameter = MaxRate
  # ---------------------------------------------------------------  
  Num=113 # number of subcatchments
  MaxRate=round(input_list[Ite,"MaxRate"],2)
  row_0=293
  for (i in 1:Num){
    row_t=row_0+(i-1)
    MaxRate_list <- unlist(strsplit(a[row_t],"\\s+"))
    MaxRate_list[2]<-MaxRate
    a[row_t]=paste(MaxRate_list,collapse=" ")
    
  }
  
  # ---------------------------------------------------------------
  # parameter = MinRate
  # ---------------------------------------------------------------  
  Num=113 # number of subcatchments
  MinRate=round(input_list[Ite,"MinRate"],3)
  row_0=293
  for (i in 1:Num){
    row_t=row_0+(i-1)
    MinRate_list <- unlist(strsplit(a[row_t],"\\s+"))
    MinRate_list[3]<-MinRate
    a[row_t]=paste(MinRate_list,collapse=" ")
    
  }
  
  # ---------------------------------------------------------------
  # parameter = Decay
  # ---------------------------------------------------------------  
  Num=113 # number of subcatchments
  Decay=round(input_list[Ite,"Decay"],2)
  row_0=293
  for (i in 1:Num){
    row_t=row_0+(i-1)
    Decay_list <- unlist(strsplit(a[row_t],"\\s+"))
    Decay_list[4]<-Decay
    a[row_t]=paste(Decay_list,collapse=" ")
    
  }
  
  # ---------------------------------------------------------------
  # parameter = DryTime
  # ---------------------------------------------------------------  
  Num=113 # number of subcatchments
  DryTime=round(input_list[Ite,"DryTime"],0)
  row_0=293
  for (i in 1:Num){
    row_t=row_0+(i-1)
    DryTime_list <- unlist(strsplit(a[row_t],"\\s+"))
    DryTime_list[5]<-DryTime
    a[row_t]=paste(DryTime_list,collapse=" ")
    
  }
  
  # ---------------------------------------------------------------
  # parameter = Roughness
  # ---------------------------------------------------------------  
  Num=195 # number of conduits
  Roughness=round(input_list[Ite,"Roughness"],0)
  row_0=735
  for (i in 1:Num){
    row_t=row_0+(i-1)
    Roughness_list <- unlist(strsplit(a[row_t],"\\s+"))
    Roughness_list[5]<-Roughness
    a[row_t]=paste(Roughness_list,collapse=" ")
    
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