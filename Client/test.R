# TODO: Add comment
# 
# Author: Ricardo Maia
###############################################################################


fibvals <- numeric(10)
fibvals[1] <- 1
fibvals[2] <- 1
for (i in 3:length(fibvals)) {
	fibvals[i] <- fibvals[i-1]+fibvals[i-2]
}
fibvals
collatz <- function(n, acc=0) {
	if(n==1) return(acc);
	collatz(ifelse(n%%2==0, n/2, 3*n +1), acc+1)} 
quiz<-collatz(27)
