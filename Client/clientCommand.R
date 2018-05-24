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

submitJob <- function(price, deadline, credibility, availability, disc, RAM, RExpression) 
{
	python.call("submitJob", client_session_id, price, deadline, credibility, availability, disc, RAM, RExpression)
}

