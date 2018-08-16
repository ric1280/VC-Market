# TODO: Add comment
# 
# Author: ricardomaia
###############################################################################


source("clientCommand.R")
source("client_config.R")

#Email - "Test@gmail.com"
#pw - "pw"

getUsers()
signup(Email, Password)
login(Email, Password)

for(machine in Machines){
	
	addMachine(machine[[1]], machine[[2]], machine[[3]], machine[[4]], machine[[5]])
				#getMachine()
	
	startVolunteer(machine[[1]])
}

