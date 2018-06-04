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



compute({ 
			
			"fibvals <- numeric(10)
			fibvals[1] <- 1
			fibvals[2] <- 1
			for (i in 3:length(fibvals)) { 
				fibvals[i] <- fibvals[i-1]+fibvals[i-2]
			} 
			fibvals"
		})



