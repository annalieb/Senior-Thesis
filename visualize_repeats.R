library(ggplot2)
library(dplyr)

getwd()
setwd("Documents/Thesis/Senior-Thesis")
all_relevant <- read.csv("all_relevant.csv")
# get max number of repetitions in a given search result list
# (ie. a single state or in the national results)
max_reps <- apply(all_relevant[,6:55], 1, max)
all_relevant$max_reps <- max_reps
hist(all_relevant$max_reps)
summary(all_relevant$max_reps)

# look at common domains
common_domains <- table(all_relevant$domain)[table(all_relevant$domain) > 150]
# make barplot

# Create a bar plot 
data <- data.frame(common_domains)
ggplot(data, aes(x = reorder(Var1, Freq), y= Freq)) +  
  coord_flip() + 
  geom_bar(stat = "identity", fill="steelblue") +
  labs(title="Most common domains", x ="Domain", y = "Count")

# view the articles with lots of repeats
repeats <- all_relevant[all_relevant$max_reps > 1,]
dim(repeats)
summary(repeats$max_reps)
length(repeats[repeats$max_reps > 2, "title"])
all_relevant$title[all_relevant$max_reps > 50]
all_relevant[all_relevant$title == "This Texas high school principal was put on administrative leave after being accused of promoting critical race theory",]

# Create a bar plot 
data <- all_relevant[all_relevant$max_reps > 50,]
ggplot(data, aes(x = reorder(title, max_reps), y= max_reps)) +  
  coord_flip() + 
  geom_bar(stat = "identity", fill="steelblue") +
  labs(title="Most common domains", x ="Domain", y = "Count")
