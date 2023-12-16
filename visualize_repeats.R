getwd()
all_relevant <- read.csv("all_relevant.csv")
# get max number of repetitions in a given search result list
# (ie. a single state or in the national results)
max_reps <- apply(all_relevant[,6:55], 1, max)
all_relevant$max_reps <- max_reps
hist(all_relevant$max_reps)
summary(all_relevant$max_reps)

# view the articles with lots of repeats
length(all_relevant$domain[all_relevant$max_reps > 1])
all_relevant$title[all_relevant$max_reps > 50]
all_relevant[all_relevant$title == "This Texas high school principal was put on administrative leave after being accused of promoting critical race theory",]
