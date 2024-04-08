# time series analysis for related terms: CRT and trans
# BASED ON: https://otexts.com/fpp2/

library(fpp2)
library(seasonal)
library(urca)
library(lmtest)
library(vars)

setwd("/Users/annalieb/Documents/Thesis/Senior-Thesis")
all_data <- read.csv("related_term_daily.csv")

sum(is.na(all_data)) # 0

# make time series objects
crt <- ts(all_data$CRT_relevant, start=c(2020, 8), frequency=365)
trans <- ts(all_data$trans_relevant, start=c(2020, 8), frequency=365)

# plot daily data
autoplot(crt) + 
  autolayer(trans)

# moving average with an order of 15 (15-MA)
# helps isolate the trend in the data (time series decomposition)
autoplot(ma(crt, 15)) + 
  autolayer(ma(trans, 15)) + 
  scale_color_hue(labels=c("trans mentions")) + 
  ylab("Proportion of total coverage \n (15-day moving avg)")

# see chapter 6.6 - STL decomposition
crt_trend <- trendcycle(stl(crt, t.window=15, s.window="periodic"))
trans_trend <- trendcycle(stl(trans, t.window=15, s.window="periodic"))
# plot the trend-cycle component
autoplot(crt_trend) + 
  autolayer(trans_trend) + 
  scale_color_hue(labels=c("trans"))

# test for log transformation (add one to eliminate zeros)
BoxCox.lambda(crt_trend + 1) 
BoxCox.lambda(trans_trend + 1) 
# Box Cox suggests lambda = -1 (inverse transformation)
crt_transformed <- (crt_trend + 1)^-1
trans_transformed <- (trans_trend + 1)^-1

autoplot(crt_transformed) + 
  autolayer(trans_transformed) + 
  scale_color_hue(labels=c("trans mentions")) + 
  ylab("\n 1 / (Proportion of total coverage + 1)")

# check for stationarity
summary(ur.kpss(crt_transformed))
summary(ur.kpss(trans_transformed))
# The test statistic (1.2788) is bigger than the 1% critical value (0.739), 
# indicating that the null hypothesis is rejected and the data are not stationary. 
# We can difference the data, and apply the test again.

# difference (for stationarity)
crt_diff <- diff(crt_transformed)
trans_diff <- diff(trans_transformed)
summary(ur.kpss(crt_diff))
summary(ur.kpss(trans_diff))
# now the test stat is much smaller than the critical value, yay!
# confirm result with ndiffs(crt_trend)

autoplot(crt_diff) + 
  autolayer(trans_diff) + 
  scale_color_hue(labels=c("trans mentions")) + 
  ylab("Differenced \n (1 / (Proportion of total coverage + 1))")

# select optimal number of lags (ie. lag order)
# VARselect() gives four different criteria: AIC, HQ, SC and FPE
# for VAR models, we prefer to use the BIC (same as SC)
# see chapter 11.2 -VAR
VARselect(crt_diff)$selection
VARselect(trans_diff)$selection

# granger causality test
# see https://search.r-project.org/CRAN/refmans/lmtest/html/grangertest.html
grangertest(crt_diff ~ trans_diff, order=9)
grangertest(trans_diff ~ crt_diff, order=9)

# how to interpret: 
# https://stats.stackexchange.com/questions/183661/how-to-understand-mutual-granger-causality

# fitted values
summary(VAR(cbind(crt_diff, trans_diff), p=9, type="none"))
