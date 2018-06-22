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
addMachine(Machine_Name, Machine_CPU, Machine_Hard_Disc, Machine_RAM, Machine_Price)
getMachine()

startVolunteer(Machine_Name)
