# TODO: Add comment
# 
# Author: ricardomaia
###############################################################################

source("clientCommand.R")
source("client_config.R")

compute <- function(mainexpression, fileName,userEnvironment=parent.frame(), mode="live" ){
	
	ls()
	
	##Save environment to send to volunteer 
	
	RData_filename = paste(fileName,"_input.RData", sep="")
	save.image(RData_filename)
	
	returnValue <- submitJob(6, 2700, 0.6544, 300000000, 4096, 1024, mainexpression, fileName, "NULL", RData_filename)

	return(returnValue)
}

compute_replication <- function(jobId, RExpression, quorum, fileName){

	##Save environment to send to volunteer 
	
	RData_filename = paste(fileName,"_input.RData", sep="")
	save.image(RData_filename)
	majorityReport(jobId, RExpression, quorum, RData_filename) 
}

single_remote_execution <- function(){
	getUsers()
	signup(Email, Password)
	login(Email, Password)


	writeLines("\n################################################################################\n")
	writeLines("These are the R files on your current directory:\n")
	writeLines(list.files(pattern = "\\.R$"))
	
	writeLines("\n################################################################################\n")
	
	if(interactive()){
		print("Choose a file to compute!")
		filename <- readline("filename: ")
		print(filename)
		
		con = file(filename, "r")
		fileTxt = readLines(con)
		code <- ""
		for(line in fileTxt){
			code = paste(code, line, sep="\n ")
		}
		
		
		close(con)
	
		compute({code}, filename)
	}

}

replication_remote_execution <- function(){
	
	getUsers()
	signup(Email, Password)
	login(Email, Password)
	
	writeLines("\n################################################################################\n")
	writeLines("These are the R files on your current directory:\n")
	writeLines(list.files(pattern = "\\.R$"))
	
	writeLines("\n################################################################################\n")

	if(interactive()){
		print("Choose a file to compute!")
		filename <- readline("filename: ")
		print(filename)
		
		con = file(filename, "r")
		fileTxt = readLines(con)
		code <- ""
		for(line in fileTxt){
			code = paste(code, line, sep="\n ")
		}
		
		
		close(con)
	
		getJobs()
		print("Choose a jobId to recompute with replication!")
		jobId <- readline("jobId: ")
		
		compute_replication(jobId, {code}, 3, filename)
	}
}











