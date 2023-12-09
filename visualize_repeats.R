getwd()
all_relevant <- read.csv("all_relevant.csv")
max_reps <- apply(all_relevant[,6:55], 1, max)
all_relevant$max_reps <- max_reps
hist(all_relevant$max_reps)
summary(all_relevant$max_reps)

# view the articles with lots of repeats
length(all_relevant$domain[all_relevant$max_reps > 1])
all_relevant$domain[all_relevant$max_reps > 50]
