setwd("/Users/annalieb/Documents/Thesis/Senior-Thesis")

labels <- read.csv("coverage_by_unique_headline.csv")
labels <- labels[, 6:7]
stances <- labels$stance
actor <- labels$actor

(table(labels) / 11704) * 100

(table(stances) / 11704) * 100
(table(actor) / 11704) * 100
