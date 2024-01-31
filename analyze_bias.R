library(jsonlite)
library("RColorBrewer")
library(rlist)

URLs <- fromJSON("coverage_by_unique_URL.json")
hist(URLs$bias_score, 
     xlab="Partisan Audience Bias Score", ylab="Count", main="",
     col=list.reverse(c("#67001F", "#67001F", "#B2182B", "#B2182B",
           "#D6604D", "#D6604D", "#F4A582", "#F4A582", 
           "#FDDBC7", "#FDDBC7", "#D1E5F0", "#D1E5F0",
           "#92C5DE", "#92C5DE", "#4393C3", "#4393C3", 
           "#2166AC", "#2166AC", "#053061", "#053061")))
table(URLs$domain)
sum(is.na(URLs$bias_score))

## get proportions of each frame 
data <- read.csv("coverage_by_unique_headline.csv",header=TRUE) 
table(data$stance) / 11704
table(data$actor) / 11704
