# ------------------------------------------------------------------------------
# percentile graphics
# ------------------------------------------------------------------------------

library(ggplot2)

Sys.info()
Sys.info()[4]

if(Sys.info()[4]=="LZ2626UECHELSVI"){
  maindir <- "C:/Users/echelsvi/git/chelsvig_urban_pesticides/"
}

swmm_path <- paste0(maindir, 'probabilistic_python/input/swmm')
vvwm_path <- paste0(maindir, 'probabilistic_python/input/vvwm')

outfalls <- c('/outfall_31_26', '/outfall_31_28', '/outfall_31_29', 
              '/outfall_31_35','/outfall_31_36', '/outfall_31_38', '/outfall_31_42')


o <- '/outfall_31_26'

for (o in outfalls){
  outfall_path <- paste0(vvwm_path,o, sep="")
  
  # load data
  # vvwm h20_conc (bif conc in water column, ug/L)
  prob_conc_h20 <- read.table(paste0(outfall_path,'/prob_conc_h20.txt', sep=''), sep=",", header=F)
  
  # vvwm benth_conc (bif conc in benthic zone, ug/L)
  prob_conc_benth <- read.table(paste0(outfall_path,'/prob_conc_benth.txt', sep=''), sep=",", header=F)
  
  # swmm runf (runf...????)
  prob_runf <- read.table(paste0(outfall_path,'/prob_runf.txt', sep=''), sep=",", header=F)
  
  
  
  # construct percentile dataframe
  dfs <- list(prob_conc_h20, prob_conc_benth, prob_runf)
  
  n <- 1
  
  for (n in 1:3){
    j <- dfs[[n]]
    dim(j) #days*sims
    
    # create blank matrix to fill with percentiles
    percentiles <- matrix(data=NA, nrow=dim(j)[1], ncol=8)
    colnames(percentiles) <- c("day", "percent.001", "percent.023", "percent.159", "percent.5",
                               "percent.841", "percent.977", "percent.999")
    percentiles <- as.data.frame(percentiles)
    
    # date format
    percentiles$day <- seq(as.Date("2009-01-01"), as.Date("2017-12-31"), by="days")
    
    
    # compute percentiles
    for (i in 1:dim(percentiles)[1]){
      p001 <- quantile(j[i,], probs=.001, na.rm=T)
      percentiles[i,2] <- p001
      
      p023 <- quantile(j[i,], probs=.023, na.rm=T)
      percentiles[i,3] <- p023
      
      p159 <- quantile(j[i,], probs=.159, na.rm=T)
      percentiles[i,4] <- p159
      
      p5 <- quantile(j[i,], probs=.5, na.rm=T)
      percentiles[i,5] <- p5
      
      p841 <- quantile(j[i,], probs=.841, na.rm=T)
      percentiles[i,6] <- p841
      
      p977 <- quantile(j[i,], probs=.977, na.rm=T)
      percentiles[i,7] <- p977
      
      p999 <- quantile(j[i,], probs=.999, na.rm=T)
      percentiles[i,8] <- p999
    }
    
    # impose a false zero
    for (k in 1:dim(percentiles)[1]){
      if (percentiles[k,2] < 1e-8){
        percentiles[k,2] <- 1e-8
      } 
    } 
    if (n == 1){
      write.table(percentiles, file= paste0(outfall_path,'/percentile_prob_conc_h20', '.txt', sep=''), quote=F, sep=",")
    } else if (n == 2){
      write.table(percentiles, file= paste0(outfall_path,'/percentile_prob_conc_benth', '.txt', sep=''), quote=F, sep=",")
    } else if (n == 3) {
      write.table(percentiles, file= paste0(outfall_path,'/percentile_prob_runf', '.txt', sep=''), quote=F, sep=",")
    }
  }
}


# plot (just 31_26 to start)
  
  
# read in deterministic output
determ_conc_h20 <- read.table(paste0(vvwm_path, '/outfall_31_26/determ_conc_h20.txt', sep=''), sep=",", header=F)
determ_conc_benth <- read.table(paste0(vvwm_path, '/outfall_31_26/determ_conc_benth.txt', sep=''), sep=",", header=F)
determ_runf <- read.table(paste0(vvwm_path, '/outfall_31_26/determ_runf.txt', sep=''), sep=",", header=F)
  
# read in probabilistic output
perc_conc_h20 <- read.table(paste0(vvwm_path, '/outfall_31_26/percentile_prob_conc_h20.txt', sep=''), sep=",", header=T)


# set colors
sd3 <- "#08519c"
sd2 <- "#4292c6"
sd1 <- "#9ecae1"
med <- "#08519c"
det <- "#d9f0a3"

# save figure as png
png(filename= paste(pwcdir, "figures/percentile_09-14_pwc_ave_h2.png", sep=""),width=20, height=10, units="in",res=300) 

# plot
pwc_pplot <- ggplot(percentiles, aes(x=day, group=1)) +
  geom_ribbon(aes(ymin=percent.001, ymax=percent.999, fill="3 SD")) +
  geom_ribbon(aes(ymin=percent.023, ymax=percent.977, fill="2 SD")) +
  geom_ribbon(aes(ymin=percent.159, ymax=percent.841, fill="1 SD")) +
  geom_line(aes(y=percent.5, color="Probabilistic Median"), linetype="solid", size=1) +
  #geom_line(aes(y=deterministic, color="Deterministic"), linetype="solid", size=1) +
  scale_y_continuous(trans="log10", breaks=trans_breaks("log10", function(x) 10^x), 
                     labels=trans_format("log10", math_format(10^.x)), limits=c(NA,10^20)) +
  scale_x_date(date_breaks="1 year", date_labels="%m-%d-%y", limits=as.Date(c('2009-01-01', '2014-12-31'))) +
  labs(title = "Daily Average Aqueous Bifenthrin Concentration in Water Columm", x = "", y = "Bifenthrin Concentration (ug/L) (log10)", color = "") +
  theme_bw() +
  theme(legend.position = "bottom") +
  scale_fill_manual(name="", values=c("3 SD"=sd3, "2 SD"=sd2, "1 SD" =sd1))
  #scale_color_manual(name="", values=c("Probabilistic Median" =med, "Deterministic"=det))
print(pwc_pplot)
dev.off()




# ------------------------------------------------------------------------------
# percentile plot: pwc Ave.Conc.benth
# ------------------------------------------------------------------------------


# --------------------------------
# data set-up
# --------------------------------

dim(pwc_ben_output) #days*sims

# create blank matrix to fill with percentiles
percentiles <- matrix(data=NA, nrow=dim(pwc_ben_output)[1], ncol=8)
colnames(percentiles) <- c("day", "percent.001", "percent.023", "percent.159", "percent.5",
                           "percent.841", "percent.977", "percent.999")
percentiles <- as.data.frame(percentiles)

# date format
percentiles$day <- seq(as.Date("2008-01-01"), as.Date("2014-12-31"), by="days")


# compute percentiles
for (i in 1:dim(percentiles)[1]){
  p001 <- quantile(pwc_ben_output[i,], probs=.001, na.rm=T)
  percentiles[i,2] <- p001
  
  p023 <- quantile(pwc_ben_output[i,], probs=.023, na.rm=T)
  percentiles[i,3] <- p023
  
  p159 <- quantile(pwc_ben_output[i,], probs=.159, na.rm=T)
  percentiles[i,4] <- p159
  
  p5 <- quantile(pwc_ben_output[i,], probs=.5, na.rm=T)
  percentiles[i,5] <- p5
  
  p841 <- quantile(pwc_ben_output[i,], probs=.841, na.rm=T)
  percentiles[i,6] <- p841
  
  p977 <- quantile(pwc_ben_output[i,], probs=.977, na.rm=T)
  percentiles[i,7] <- p977
  
  p999 <- quantile(pwc_ben_output[i,], probs=.999, na.rm=T)
  percentiles[i,8] <- p999
}
percentiles$percent.001 <- percentiles$percent.001*1000000 #convert units to ug/L 
percentiles$percent.023 <- percentiles$percent.023*1000000 
percentiles$percent.159 <- percentiles$percent.159*1000000 
percentiles$percent.5 <- percentiles$percent.5*1000000 
percentiles$percent.841 <- percentiles$percent.841*1000000  
percentiles$percent.977 <- percentiles$percent.977*1000000  
percentiles$percent.999 <- percentiles$percent.999*1000000  




# read in deterministic output
determ <- read.csv("C:/Users/echelsvi/git/yuan_urban_pesticides/deterministic/input/FOL002/outputs/output_FOL002_parent_only_Custom_Parent_daily.csv",
                   header= FALSE, sep= ",", skip = 5, stringsAsFactors = FALSE, row.names=NULL)
colnames(determ) <- c("Depth(m)","Ave.Conc.H20","Ave.Conc.benth","Peak.Conc.H20")
determ <- as.data.frame(determ)

# subset Ave.conc.H20, add to percentiles df
percentiles$deterministic <- determ$Ave.Conc.benth*1000000 #convert units to ug/L


# impose a false zero
for (i in 1:dim(percentiles)[1]){
  if (percentiles[i,2] < 1e-8){
    percentiles[i,2] <- 1e-8
  } 
} 


# --------------------------------
# plot
# --------------------------------

# set colors
sd3 <- "#6a51a3"
sd2 <- "#807dba"
sd1 <- "#bcbddc"
med <- "#6a51a3"
det <- "#d9f0a3"


# save figure as png
png(filename= paste(pwcdir, "figures/percentile_09-14_pwc_ave_benthic.png", sep=""),width=20, height=10, units="in",res=300) 

# plot
pwc_pplot <- ggplot(percentiles, aes(x=day, group=1)) +
  geom_ribbon(aes(ymin=percent.001, ymax=percent.999, fill="3 SD")) +
  geom_ribbon(aes(ymin=percent.023, ymax=percent.977, fill="2 SD")) +
  geom_ribbon(aes(ymin=percent.159, ymax=percent.841, fill="1 SD")) +
  geom_line(aes(y=percent.5, color="Probabilistic Median"), linetype="solid", size=1) +
  geom_line(aes(y=deterministic, color="Deterministic"), linetype="solid", size=1) +
  scale_x_date(date_breaks="1 year", date_labels="%m-%d-%y", limits=as.Date(c('2009-01-01', '2014-12-31'))) +
  scale_y_continuous(trans="log10", breaks=trans_breaks("log10", function(x) 10^x), 
                     labels=trans_format("log10", math_format(10^.x)), limits=c(NA,5)) +
  labs(title = "Daily Average Aqueous Bifenthrin Concentration in Benthic Zone", x = "", y = "Bifenthrin Concentration (ug/L) (log10)", color = "") +
  theme_bw() +
  theme(legend.position = "bottom") +
  scale_fill_manual(name="", values=c("3 SD"=sd3, "2 SD"=sd2, "1 SD" =sd1))+
  scale_color_manual(name="", values=c("Probabilistic Median" =med, "Deterministic"=det))
print(pwc_pplot)
dev.off()





# ------------------------------------------------------------------------------
# the end
# ------------------------------------------------------------------------------