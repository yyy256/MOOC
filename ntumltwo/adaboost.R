library(RCurl)
a1 <- getURI("https://d396qusza40orc.cloudfront.net/ntumltwo/hw2_data/hw2_adaboost_train.dat")
a2 <- getURI("https://d396qusza40orc.cloudfront.net/ntumltwo/hw2_data/hw2_adaboost_test.dat")
train <- read.table(text = a1)
test <- read.table(text = a2)

library(ggplot2)
ggplot(aes(x=V1,y=V2,shape=as.factor(V3),color=as.factor(V3)), data=train) + geom_point()

library(dplyr)
library(magrittr)


for (j in c("V1", "V2")){
  all_theta <- na.omit((sort(train[,j]) + lead(sort(train[,j])))/2)
  for (theta in all_theta){
    train1 <- train %>% mutate(V4 = ifelse(train[,j] >= i, -1, 1))
    r <- with(train1, sum(V3 != V4)/nrow(train1))   
    res <- c(res, r, 1-r)
  }
}


U <- list()
epsilon <- c()
u <- rep(1/100, 100)
G <- 0
test_G <- 0
i <- 1
while (i <= 300){
  err_r <- Inf
  for (j in c("V1", "V2")){
    all_theta <- na.omit((sort(train[,j]) + lead(sort(train[,j])))/2)
    for (s in c(-1, 1)){
      for (theta in all_theta){
        g1 <- s*sign(train[,j] - theta)
        r <- (t(u) %*% as.numeric(train$V3 != g1)) / sum(u)
        if (r < err_r) {err_r <- r; best_g <- g1; s1<- s; theta1<-theta; v=j}
      }
    }
    alpha <- 0.5 * log((1 - err_r) / err_r) 
  }
  test_g <- s1 * sign(test[,v] - theta1)
  epsilon1 <- (t(u) %*% as.numeric(train$V3 != best_g)) / sum(u)
  t <- sqrt((1-err_r)/err_r)
  u <- u * ifelse(train$V3 == best_g, 1/t, t)
  U[[i+1]] <- u
  epsilon <- c(epsilon, err_r) 
  G <- G + alpha*best_g
  test_G <- test_G + alpha*test_g
  i <- i + 1
}
e_in <- sum(train$V3 != sign(G)) / nrow(train)
e_out <- sum(test$V3 != sign(test_G)) / nrow(test)
