# interrater agreement - labeling v3 
# https://cran.r-project.org/web/packages/irr/irr.pdf#page.16
# Krippendorff’s alpha: useful when there are multiple raters and multiple possible ratings
# Same metric used in Liu et al. 2019
# 11/28/2023

library("irr")

setwd("/Users/annalieb/Documents/Thesis/Harvard-dataverse-repo.nosync")

############ Read in coding files with labels ############
r1 <- read.csv("other_data/coding/r1_coding.csv",header=TRUE)
r2 <- read.csv("other_data/coding/r2_coding.csv",header=TRUE)
gpt <- read.csv("other_data/coding/GPT_coding.csv",header=TRUE)
consensus <- read.csv("other_data/coding/consensus_coding.csv", header=TRUE)

clean_labels <- function(df) {
  # remove rows that are not relevant: 32, 38, 39, 50, 68, 72, 131, 133
  df <- df[-c(32, 38, 39, 50, 68, 72, 131, 133),]
  # remove the first duplicated instance 
  # (label was generated later, with more coding experience)
  df <- df[-which(duplicated(df$Title, fromLast = TRUE)),]
  # remove rows that have misc. labeller notes
  df <- df[, 1:5]
  # combine policy with elections
  df$action[df$action == "elections"] <- "policy & legal"
  # reset indices
  row.names(df) <- NULL
  return(df)
}

r1 <- clean_labels(r1)
r2 <- clean_labels(r2)

sum(r1$Title != gpt$Title & r2$Title != gpt$Title)

convert_labels <- function(df) {
  df$actor[df$actor == "educational practitioners"] <- 0
  df$actor[df$actor == "political influencers"] <- 1
  df$actor[df$actor == "impacted actors"] <- 2
  df$actor[df$actor == "none / other"] <- 3
  
  df$action[df$action == "protest / speaking out"] <- 0
  df$action[df$action == "policy & legal"] <- 1
  df$action[df$action == "threats/extent"] <- 2
  df$action[df$action == "none/other"] <- 3
  
  df$action.direction[df$action.direction=="anti-CRT"] <- -1
  df$action.direction[df$action.direction=="neutral"] <- 0
  df$action.direction[df$action.direction=="defending CRT"] <- 1
  
  df$headline.stance[df$headline.stance=="anti-CRT"] <- -1
  df$headline.stance[df$headline.stance=="neutral"] <- 0
  df$headline.stance[df$headline.stance=="defending CRT"] <- 1
  
  return(df)
}

convert_gpt_labels <- function(df) {
  df$actor[df$actor == "<EDUCATIONAL PRACTITIONER>"] <- 0
  df$actor[df$actor == "<POLITICAL INFLUENCER>"] <- 1
  df$actor[df$actor == "<IMPACTED ACTOR>"] <- 2
  df$actor[df$actor == "<NONE/OTHER>"] <- 3
  
  df$action[df$action == "<PROTEST / SPEAKING OUT>"] <- 0
  df$action[df$action == "<POLICY / LEGAL / ELECTIONS>"] <- 1
  df$action[df$action == "<THREATS / EXTENT>"] <- 2
  df$action[df$action == "<NONE/OTHER>"] <- 3
  
  df$action.direction[df$action.direction=="<ANTI-CRT>"] <- -1
  df$action.direction[df$action.direction=="<NEUTRAL>"] <- 0
  df$action.direction[df$action.direction=="<DEFENDING CRT>"] <- 1
  
  df$headline.stance[df$headline.stance=="<ANTI-CRT>"] <- -1
  df$headline.stance[df$headline.stance=="<NEUTRAL>"] <- 0
  df$headline.stance[df$headline.stance=="<DEFENDING CRT>"] <- 1
  
  return(df)
}

r1 <- convert_labels(r1)
r2 <- convert_labels(r2)
consensus <- convert_labels(consensus)
gpt <- convert_gpt_labels(gpt)

# make variables as.factor
col_names <- names(r1)[2:5]
r1[col_names] <- lapply(r1[col_names], factor)
r2[col_names] <- lapply(r2[col_names], factor)
gpt[col_names] <- lapply(gpt[col_names], factor)
consensus[col_names] <- lapply(consensus[col_names], factor)

############ Calculate alpha ############

## Validity concerns with rater 2; coding was being entered concurrently 
# during group meeting to find consensus

# For fully-crossed designs with three or more coders, Light (1971) suggests 
# computing kappa for all coder pairs then using the arithmetic mean of 
# these estimates to provide an overall index of agreement. 
# ... Light’s solution can easily be implemented by computing kappa for all 
# coder pairs using statistical software then manually computing the arithmetic mean.

# actors alpha: 0.673
actors <- cbind(r1$actor, r2$actor)
actors_alpha <- kappa2(actors)
actors_alpha

# with gpt: 0.696
a1 <- kappa2(cbind(r1$actor, r2$actor))$value
a2 <- kappa2(cbind(r1$actor, gpt$actor))$value
a3 <- kappa2(cbind(gpt$actor, r2$actor))$value
mean(c(a1, a2, a3))

# action alpha: 0.609
kappa2(cbind(r1$action, r2$action))

# action direction: 0.681 
kappa2(cbind(r1$action.direction, r2$action.direction))

# headline stance: 0.742 
kappa2(cbind(r1$headline.stance, r2$headline.stance))
# with gpt: 0.662
a1 <- kappa2(cbind(r1$headline.stance, r2$headline.stance))$value
a2 <- kappa2(cbind(r1$headline.stance, gpt$headline.stance))$value
a3 <- kappa2(cbind(gpt$headline.stance, r2$headline.stance))$value
mean(c(a1, a2, a3))
