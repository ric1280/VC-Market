# TODO: Add comment
# 
# Author: ricardomaia
###############################################################################

source("commandsScript.R")

#library(ggplot2)
#library(car)

compute <- function(mainexpression, userEnvironment=parent.frame(), mode="live" ){
	
	#print(mainexpression)
	
	
	#returnValue <- eval(parse(text = mainexpression))
	
	ls()
	
	returnValue <- submitJob(6, 2700, "NULL", "NULL", 4096, 1024, mainexpression)

	return(returnValue)
}

#collatz <- function(n, acc=0) {
#	if(n==1) return(acc);
#	collatz(ifelse(n%%2==0, n/2, 3*n +1), acc+1)} 



compute({ 
			
			"fibvals <- numeric(10)
			fibvals[1] <- 1
			fibvals[2] <- 1
			for (i in 3:length(fibvals)) { 
				fibvals[i] <- fibvals[i-1]+fibvals[i-2]
			} 
			"
		})




# conjectura de collatz
#
# if n == numero par 
#    n = n/2
# if n == impar 
#    n = 3n + 1
#
# computar o número de iterações
