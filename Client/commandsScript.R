# TODO: Add comment
# 
# Author: ricardomaia
###############################################################################


source("clientCommand.R")


#Email - "Test@gmail.com"
#pw - "pw"

getUsers()
signup("Test@gmail.com", "pw")
login("Test@gmail.com", "pw")
addMachine("Machine1", 500000000, 100000, 2048, 5)
getMachine()

startVolunteer("Machine1")
