# interrater agreement - labeling v3 
# https://cran.r-project.org/web/packages/irr/irr.pdf#page.16
# Krippendorff’s alpha: useful when there are multiple raters and multiple possible ratings
# Same metric used in Liu et al. 2019
# 11/28/2023

library("irr")

setwd("/Users/annalieb/Documents/Thesis/Senior-Thesis")

############ Read in v3 files ############
r1_v3 <- read.csv("coding/Anna_coding_v3.csv",header=TRUE)
r2_v3 <- read.csv("coding/Ariel_coding_v3.csv",header=TRUE)
r3_v3 <- read.csv("coding/Tarishi_coding_v3.csv",header=TRUE)

# remove rows that have misc. labeler notes
r1_v3 <- r1_v3[1:50, 1:5]
r2_v3 <- r2_v3[1:50, 1:5]
r3_v3 <- r3_v3[1:50, 1:5]
# remove index 32, 38, 39, and 50
r1_v3 <- r1_v3[-c(32, 38, 39, 50),]
r2_v3 <- r2_v3[-c(32, 38, 39, 50),]
r3_v3 <- r3_v3[-c(32, 38, 39, 50),]
# combine policy with elections
r1_v3$action[r1_v3$action == "elections"] <- "policy & legal"
r2_v3$action[r2_v3$action == "elections"] <- "policy & legal"
r3_v3$action[r3_v3$action == "elections"] <- "policy & legal"

# make variables as.factor
col_names <- names(r1_v3)
r1_v3[col_names] <- lapply(r1_v3[col_names], factor)
r2_v3[col_names] <- lapply(r2_v3[col_names], factor)
r3_v3[col_names] <- lapply(r3_v3[col_names], factor)

# convert ordinal variables to -1 (anti), 1 (defending), and 0 (neutral)
levels(r1_v3$action.direction) <- c(-1, 1, 0)
levels(r2_v3$action.direction) <- c(-1, 1, 0)
levels(r3_v3$action.direction) <- c(-1, 1, 0)
levels(r1_v3$headline.stance) <- c(-1, 1, 0)
levels(r2_v3$headline.stance) <- c(-1, 1, 0)
levels(r3_v3$headline.stance) <- c(-1, 1, 0)

############ Read in v4 files ############
r1_v4 <- read.csv("coding/Anna_coding_v4.csv",header=TRUE)
r2_v4 <- read.csv("coding/Ariel_coding_v4.csv",header=TRUE)
r3_v4 <- read.csv("coding/Tarishi_coding_v4.csv",header=TRUE)

# EDIT THIS SECTION AFTER FINAL LABELS ARE IN #
# remove rows that have misc. labeler notes
r1_v4 <- r1_v4[1:50, 1:5]
r2_v4 <- r2_v4[1:50, 1:5]
r3_v4 <- r3_v4[1:50, 1:5]
# remove index 18, 22
r1_v4 <- r1_v4[-c(18, 22),]
r2_v4 <- r2_v4[-c(18, 22),]
r3_v4 <- r3_v4[-c(18, 22),]
# combine policy with elections
r1_v4$action[r1_v4$action == "elections"] <- "policy & legal"
r2_v4$action[r2_v4$action == "elections"] <- "policy & legal"
r3_v4$action[r3_v4$action == "elections"] <- "policy & legal"

# make variables as.factor
col_names <- names(r1_v4)
r1_v4[col_names] <- lapply(r1_v4[col_names], factor)
r2_v4[col_names] <- lapply(r2_v4[col_names], factor)
r3_v4[col_names] <- lapply(r3_v4[col_names], factor)

# convert ordinal variables to -1 (anti), 1 (defending), and 0 (neutral)
levels(r1_v4$action.direction) <- c(-1, 1, 0)
levels(r2_v4$action.direction) <- c(-1, 1, 0)
levels(r3_v4$action.direction) <- c(-1, 1, 0)
levels(r1_v4$headline.stance) <- c(-1, 1, 0)
levels(r2_v4$headline.stance) <- c(-1, 1, 0)
levels(r3_v4$headline.stance) <- c(-1, 1, 0)

## Combine results
r1 <- rbind(r1_v3, r1_v4)
r2 <- rbind(r2_v3, r2_v4)
r3 <- rbind(r3_v3, r3_v4)

## Validity concerns with rater 2; coding was being entered concurrently 
# during group meeting to find consensus

# actors alpha: 0.695 
actors <- t(cbind(r1$actor, r3$actor))
actors_alpha <- kripp.alpha(actors, method="nominal")
actors_alpha

# action alpha: 0.636 
action <- t(cbind(r1$action, r3$action))
action_alpha <- kripp.alpha(action, method="nominal")
action_alpha

# action direction: 0.716 
direction <- t(cbind(r1$action.direction, r3$action.direction))
direction_alpha <- kripp.alpha(direction, method="ordinal")
direction_alpha

# headline stance: 0.862 
stance <- t(cbind(r1$headline.stance, r3$headline.stance))
stance_alpha <- kripp.alpha(stance, method="ordinal")
stance_alpha
