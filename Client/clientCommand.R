# TODO: Add comment
# 
# Author: ricardomaia
###############################################################################


suppressWarnings(library("rPython"))

python.load("../Client/client.py")
python.load("../Client/codeParser.py")


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

submitJob <- function(price, deadline, credibility, CPU, disc, RAM, RExpression, fileName, meanUptime, RData_fileName) 
{
	
	variables_list <- python.call("getVariablesfromCode", RExpression)
	print(paste("variables list:", variables_list))
	
	
	returning_msg <- python.call("submitJob", client_session_id, price, deadline, credibility, CPU, disc, RAM, RExpression, fileName, meanUptime, RData_fileName, variables_list)
	if(returning_msg == "Job executed successfully"){
		load('output.RData', envir=call_env)
		print("Job loaded successfully")
		
		symbol_list<-ls()
		print(symbol_list)
		
	}
}

getJobs <- function(){
	job_list <- python.call("getJobs", client_session_id)
	
	if(length(job_list) == 0){
		print("You have no jobs available")
		
	}else{

		tab<-c()
		if(length(job_list[[1]])==1){
			
			tab<-rbind(tab,unlist(job_list))
		}else{
			for(i in 1:length(job_list)){			
				tab<-rbind(tab,unlist(job_list[[i]]))
			}
		}	
		
		colnames(tab)<-c("JobId","Computed file","Submission time", "Status")
		#write.table(as.data.frame(tab), row.names=F, col.names=T, sep="\t")
		print(as.data.frame(tab),row.names = FALSE)
	
	}

	
}

loadJob <- function(jobId){
	#Check if the RData file already exists on client side
	
	file_name <- paste(jobId,'_output.RData',sep="")
	if (!file.exists(file_name)) {
		job_msg <- python.call("loadJob", client_session_id, jobId)
		if(job_msg == "OK"){
			print(paste("Job with id:",jobId, " was downloaded to ", getwd(), "with filename: ", file_name))
		}
	}else{
		print("RData file already exists - Loading file loacally...")
		job_msg <- "OK"
	}
	
	if(job_msg != "OK"){
		print(job_msg)
		
	}else{
		job<-load( file_name, envir=call_env)
		print("Job loaded successfully")
		
		print("Objects loaded: ")
		print(job)
		
		#symbol_list<-ls()
		#print(symbol_list)
	}
	
}
