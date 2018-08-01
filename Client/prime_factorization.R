# TODO: Add comment
# 
# Author: ricar
###############################################################################


pfact <- function(number) 
{
	
	factors <- c()
	factor <- 2
	
	if(number == 1)
		return (1)
	
	while( number != 1){
		
		if(number%%factor == 0){
			number <- number/factor;
			factors <- c(factors, factor)	
		}else{
			factor <- factor + 1
		}
	}
	
	return (factors)
	
	
	
}

#result <- pfact(234536332)

result <- pfact(quiz)