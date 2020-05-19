

surf <- read.csv("C:/Users/echelsvi/git/chelsvig_urban_pesticides/observed_data/SURF_water.csv", header=TRUE, sep=",")

# All Sites of Interest
surf_bif <- surf[surf$Chemical_name == "bifenthrin", ]
placer_bif <- surf_bif[surf_bif$County_name == "Placer", ]

write.csv(placer_bif, "C:/Users/echelsvi/git/chelsvig_urban_pesticides/observed_data/SURF_water_placer_bifenthrin.csv")


# Specific Sites
# 31_26
ms1 <- surf[surf$Site_code == "31_26" , ]
ms1$Date <- as.Date( as.character(ms1$Sample_date), "%Y-%m-%d")
site1 <- ms1[ms1$Chemical_name == "bifenthrin",]
site1 <- site1[order(site1$Date),]

# 31_27
aside <- surf[surf$Site_code == "31_27" , ]
aside$Date <- as.Date( as.character(aside$Sample_date), "%Y-%m-%d")
aside <- aside[aside$Chemical_name == "bifenthrin",]
aside <- aside[order(aside$Date),]



# 31_28
ms2 <- surf[surf$Site_code == "31_28" , ]
ms2$Date <- as.Date( as.character(ms2$Sample_date), "%Y-%m-%d")
site2 <- ms2[ms2$Chemical_name == "bifenthrin",]
site2 <- site2[order(site2$Date),]


# 31_30
aside <- surf[surf$Site_code == "31_30" , ]
aside$Date <- as.Date( as.character(aside$Sample_date), "%Y-%m-%d")
aside <- aside[aside$Chemical_name == "bifenthrin",]
aside <- aside[order(aside$Date),]

# 31_31
aside <- surf[surf$Site_code == "31_31" , ]
aside$Date <- as.Date( as.character(aside$Sample_date), "%Y-%m-%d")
aside <- aside[aside$Chemical_name == "bifenthrin",]
aside <- aside[order(aside$Date),]

# 31_41
aside <- surf[surf$Site_code == "31_41" , ]
aside$Date <- as.Date( as.character(aside$Sample_date), "%Y-%m-%d")
aside <- aside[aside$Chemical_name == "bifenthrin",]
aside <- aside[order(aside$Date),]







# 31_29
ms2 <- surf[surf$Site_code == "31_29" , ]
ms2$Date <- as.Date( as.character(ms2$Sample_date), "%Y-%m-%d")
site2 <- ms2[ms2$Chemical_name == "bifenthrin",]
site2 <- site2[order(site2$Date),]

# 31_35
ms2 <- surf[surf$Site_code == "31_35" , ]
ms2$Date <- as.Date( as.character(ms2$Sample_date), "%Y-%m-%d")
site2 <- ms2[ms2$Chemical_name == "bifenthrin",]
site2 <- site2[order(site2$Date),]

# 31_36
ms2 <- surf[surf$Site_code == "31_36" , ]
ms2$Date <- as.Date( as.character(ms2$Sample_date), "%Y-%m-%d")
site2 <- ms2[ms2$Chemical_name == "bifenthrin",]
site2 <- site2[order(site2$Date),]

# 31_37
ms2 <- surf[surf$Site_code == "31_37" , ]
ms2$Date <- as.Date( as.character(ms2$Sample_date), "%Y-%m-%d")
site2 <- ms2[ms2$Chemical_name == "bifenthrin",]
site2 <- site2[order(site2$Date),]

# 31_38
ms2 <- surf[surf$Site_code == "31_38" , ]
ms2$Date <- as.Date( as.character(ms2$Sample_date), "%Y-%m-%d")
site2 <- ms2[ms2$Chemical_name == "bifenthrin",]
site2 <- site2[order(site2$Date),]

# 31_42
ms2 <- surf[surf$Site_code == "31_42" , ]
ms2$Date <- as.Date( as.character(ms2$Sample_date), "%Y-%m-%d")
site2 <- ms2[ms2$Chemical_name == "bifenthrin",]
site2 <- site2[order(site2$Date),]

# 31_43
ms2 <- surf[surf$Site_code == "31_43" , ]
ms2$Date <- as.Date( as.character(ms2$Sample_date), "%Y-%m-%d")
site2 <- ms2[ms2$Chemical_name == "bifenthrin",]
site2 <- site2[order(site2$Date),]
