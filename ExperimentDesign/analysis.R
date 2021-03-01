summary(all_log)

library(ggplot2)

ggplot(all_log, aes(x=visualSearchTime),) +
  geom_density()

ggplot(all_log, aes(x=visualSearchTime, color=VV)) +
  geom_density()

summarySE <- function(data=NULL, measurevar, groupvars=NULL, na.rm=FALSE,
                      conf.interval=.95, .drop=TRUE) {
  require(plyr)
  
  # New version of length which can handle NA's: if na.rm==T, don't count them
  length2 <- function (x, na.rm=FALSE) {
    if (na.rm) sum(!is.na(x))
    else       length(x)
  }
  
  # This does the summary. For each group's data frame, return a vector with
  # N, mean, and sd
  datac <- ddply(data, groupvars, .drop=.drop,
                 .fun = function(xx, col) {
                   c(N    = length2(xx[[col]], na.rm=na.rm),
                     mean = mean   (xx[[col]], na.rm=na.rm),
                     sd   = sd     (xx[[col]], na.rm=na.rm)
                   )
                 },
                 measurevar
  )
  
  # Rename the "mean" column    
  datac <- rename(datac, c("mean" = measurevar))
  
  datac$se <- datac$sd / sqrt(datac$N)  # Calculate standard error of the mean
  
  # Confidence interval multiplier for standard error
  # Calculate t-statistic for confidence interval: 
  # e.g., if conf.interval is .95, use .975 (above/below), and use df=N-1
  ciMult <- qt(conf.interval/2 + .5, datac$N-1)
  datac$ci <- datac$se * ciMult
  
  return(datac)
}

normDataWithin <- function(data=NULL, idvar, measurevar, betweenvars=NULL,
                           na.rm=FALSE, .drop=TRUE) {
  require(plyr)
  
  # Measure var on left, idvar + between vars on right of formula.
  data.subjMean <- ddply(data, c(idvar, betweenvars), .drop=.drop,
                         .fun = function(xx, col, na.rm) {
                           c(subjMean = mean(xx[,col], na.rm=na.rm))
                         },
                         measurevar,
                         na.rm
  )
  
  # Put the subject means with original data
  data <- merge(data, data.subjMean)
  
  # Get the normalized data in a new column
  measureNormedVar <- paste(measurevar, "_norm", sep="")
  data[,measureNormedVar] <- data[,measurevar] - data[,"subjMean"] +
    mean(data[,measurevar], na.rm=na.rm)
  
  # Remove this subject mean column
  data$subjMean <- NULL
  
  return(data)
}

summarySEwithin <- function(data=NULL, measurevar, betweenvars=NULL, withinvars=NULL,
                            idvar=NULL, na.rm=FALSE, conf.interval=.95, .drop=TRUE) {
  
  # Ensure that the betweenvars and withinvars are factors
  factorvars <- vapply(data[, c(betweenvars, withinvars), drop=FALSE],
                       FUN=is.factor, FUN.VALUE=logical(1))
  
  if (!all(factorvars)) {
    nonfactorvars <- names(factorvars)[!factorvars]
    message("Automatically converting the following non-factors to factors: ",
            paste(nonfactorvars, collapse = ", "))
    data[nonfactorvars] <- lapply(data[nonfactorvars], factor)
  }
  
  # Get the means from the un-normed data
  datac <- summarySE(data, measurevar, groupvars=c(betweenvars, withinvars),
                     na.rm=na.rm, conf.interval=conf.interval, .drop=.drop)
  
  # Drop all the unused columns (these will be calculated with normed data)
  datac$sd <- NULL
  datac$se <- NULL
  datac$ci <- NULL
  
  # Norm each subject's data
  ndata <- normDataWithin(data, idvar, measurevar, betweenvars, na.rm, .drop=.drop)
  
  # This is the name of the new column
  measurevar_n <- paste(measurevar, "_norm", sep="")
  
  # Collapse the normed data - now we can treat between and within vars the same
  ndatac <- summarySE(ndata, measurevar_n, groupvars=c(betweenvars, withinvars),
                      na.rm=na.rm, conf.interval=conf.interval, .drop=.drop)
  
  # Apply correction from Morey (2008) to the standard error and confidence interval
  #  Get the product of the number of conditions of within-S variables
  nWithinGroups    <- prod(vapply(ndatac[,withinvars, drop=FALSE], FUN=nlevels,
                                  FUN.VALUE=numeric(1)))
  correctionFactor <- sqrt( nWithinGroups / (nWithinGroups-1) )
  
  # Apply the correction factor
  ndatac$sd <- ndatac$sd * correctionFactor
  ndatac$se <- ndatac$se * correctionFactor
  ndatac$ci <- ndatac$ci * correctionFactor
  
  # Combine the un-normed means with the normed results
  merge(datac, ndatac)
}

all_log_summary <- summarySEwithin(all_log, measurevar="visualSearchTime", withinvars=c("VV","OC"), idvar="ParticipantID")

View(all_log_summary)

all_log_summary$OC <- as.factor(all_log_summary$OC)

# filter out data for keeping trials in Lens=â€œFLâ€? condition only
liner_data2 <- all_log[all_log$VV == "OrientationSize", ]
liner_data2$OC <- as.numeric(liner_data2$OC)
linearmodel2 <- lm(liner_data2$visualSearchTime ~ liner_data2$OC)
summary(linearmodel2)

ggplot(liner_data2, aes(x=OC, y=visualSearchTime)) + # map chart attributes to data
  scale_x_continuous(breaks = seq(1,3,by = 1)) +
  theme(text = element_text(size=30), legend.position = "top") + # adjust label size and legend position
  geom_point(shape=1) + # add a point layer (one circle per data point)
  geom_smooth(method=lm, se=FALSE) # add a regression line layer

# filter out data for keeping trials in Lens=â€œFLâ€? condition only
fisheye_data <- all_log_summary[all_log_summary$VV == "OrientationSize", ]
linearmodel <- lm(fisheye_data$visualSearchTime ~ fisheye_data$OC)
summary(linearmodel)

# plot visualSearchTime as a linear function of oc
ggplot(all_log, aes(x=OC, y=visualSearchTime)) + # map chart attributes to data
  theme(text = element_text(size=30), legend.position = "top") + # adjust label size and legend position
  geom_point(shape=1) + # add a point layer (one circle per data point)
  geom_smooth(method=lm, se=FALSE) # add a regression line layer

ggsave("linearregression_global.pdf", plot = last_plot())

# plot PointingTime as a linear function of ID per Lens
ggplot(all_log, aes(x=OC, y=visualSearchTime, color=VV)) + # map chart attributes to data
  theme(text = element_text(size=30), legend.position = "top") + # adjust label size and legend position
  geom_point(shape=1) + # add a point layer (one circle per data point)
  geom_smooth(method=lm, se=FALSE) # add a regression line layer

ggsave("linearregression_perVV.pdf", plot = last_plot())


## Visualize mean pointing time per condition
all_log_summary <- summarySEwithin(all_log, measurevar="visualSearchTime", withinvars=c("VV"), idvar="ParticipantID")
all_log_summary
ggplot(all_log_summary, aes(x=VV, y=visualSearchTime, fill=VV)) +
  geom_bar(stat="identity") + # plot data as is using a bar plot layer
  geom_errorbar(aes(ymin=visualSearchTime-ci, ymax=visualSearchTime+ci), width=.2) + # plot error bar layer using the confidence intervals
  theme(text = element_text(size=20)) # make text smaller

ggsave("mean_per_vv.pdf", plot = last_plot())

all_log_summary <- summarySEwithin(all_log, measurevar="visualSearchTime", withinvars=c("OC"), idvar="ParticipantID")
all_log_summary
ggplot(all_log_summary, aes(x=OC, y=visualSearchTime, fill=OC)) +
  geom_bar(stat="identity") + # plot data as is using a bar plot layer
  geom_errorbar(aes(ymin=visualSearchTime-ci, ymax=visualSearchTime+ci), width=.2) + # plot error bar layer using the confidence intervals
  theme(text = element_text(size=20)) # make text smaller

ggsave("mean_per_vv.pdf", plot = last_plot())

all_log_summary <- summarySEwithin(all_log, measurevar="visualSearchTime", withinvars=c("VV","OC"), idvar="ParticipantID")
all_log_summary
ggplot(all_log_summary, aes(x=VV, y=visualSearchTime, fill=OC)) +
  geom_bar(stat="identity", position=position_dodge()) + # plot data as is using a bar plot layer (use position_dodge to display conditions side-by-side)
  geom_errorbar(aes(ymin=visualSearchTime-ci, ymax=visualSearchTime+ci), width=.2, position=position_dodge(.9)) + # plot error bar layer using the confidence intervals
  theme(text = element_text(size=20)) # make text smaller

ggsave("mean_per_vv_and_oc.pdf", plot = last_plot())

### H3 ###
## Two-way repeated measures ANOVA
library(ez)
all_log$OC <- as.factor(all_log$OC)
ezANOVA(data=all_log,dv=.(visualSearchTime), wid=.(ParticipantID), within =.(VV,OC), detailed=TRUE, type=1)

# post-hoc tests
data_OrientationSize <- all_log[all_log$VV == "OrientationSize",]
pairwise.t.test(data_OrientationSize$visualSearchTime,data_OrientationSize$OC,paired=TRUE)

data_Small <- all_log[all_log$OC == "Small",]
pairwise.t.test(data_Small$visualSearchTime,data_Small$VV,paired=TRUE)

data_Medium <- all_log[all_log$OC == "Medium",]
pairwise.t.test(data_Medium$visualSearchTime,data_Medium$VV,paired=TRUE)

data_Large <- all_log[all_log$OC == "Large",]
pairwise.t.test(data_Large$visualSearchTime,data_Large$VV,paired=TRUE)

### H1 ###
## One-way repeated measures ANOVA
data1 <- all_log[all_log$VV == "Size",]
library(ez) # requires having installed package "ez"
ezANOVA(data=data1,dv=.(visualSearchTime), wid=.(ParticipantID), within =.(OC), detailed=TRUE)
pairwise.t.test(data1$visualSearchTime,data2$OC,paired=TRUE)

### H2 ###
## One-way repeated measures ANOVA
data2 <- all_log[all_log$VV == "Orientation",]
library(ez) # requires having installed package "ez"
ezANOVA(data=data2,dv=.(visualSearchTime), wid=.(ParticipantID), within =.(OC), detailed=TRUE)
pairwise.t.test(data2$visualSearchTime,data2$OC,paired=TRUE)