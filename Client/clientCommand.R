# TODO: Add comment
# 
# Author: ricardomaia
###############################################################################


suppressWarnings(library("rPython"))

python.load("../Client/client.py")


###############################COMMANDS################################
### getUser()
### signup(Email, pw)
### login(Email, pw)

### Login dependent functions:
### addMachine(machineName, CPU, Disc, RAM, price)
### getMachine()
### startVolunteer(machineName)
### submitJobs(price, deadline, credibility, availability, disc, RAM)
#######################################################################

## store call environment in variable
call_env <- environment()

client_session_id <- "NULL"

getUsers <- function() 
{
	python.call("getUsers")
}

signup <- function(Email, pw) 
{
	python.call("signup", Email, pw)
}

login <- function(Email, pw) 
{
	assign("client_session_id", python.call("login", Email, pw), envir = .GlobalEnv)
}

client_session_id

addMachine <- function(machineName, CPU, Disc, RAM, price) 
{
	python.call("addMachine", client_session_id, machineName, CPU, Disc, RAM, price)
}

getMachine <- function() 
{
	python.call("getMachine", client_session_id)
}

startVolunteer <- function(machineName) 
{
	python.call("startVolunteer", client_session_id, machineName)
}

submitJob <- function(price, deadline, credibility, CPU, disc, RAM, RExpression, fileName) 
{
	
	
	returning_msg <- python.call("submitJob", client_session_id, price, deadline, credibility, CPU, disc, RAM, RExpression, fileName)
	if(returning_msg == "Job executed successfully"){
		load('output.RData', envir=call_env)
		print("Job loaded successfully")
		
		symbol_list<-ls()
		print(symbol_list)
		
	}
}

getJobs <- function(){
	job_list <- python.call("getJobs", client_session_id)
	for(job in 1:nrow(job_list)) {
		
		print("####################")
		
		print(paste("JobId:" ,  job_list[job, 1]))
		print(paste("File computed:" ,  job_list[job, 2]))
		print(paste("Submission time:" ,  job_list[job, 3]))
		
		
	}
	
	print(job_list)
}
