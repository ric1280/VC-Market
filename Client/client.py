'''
Created on 03/04/2018

@author: ricar
'''

import xmlrpclib
import os
import subprocess

import time
import pickle
from platform import machine


#from OffloadingPredictor.threads import startbandwidthScout
#from OffloadingPredictor.threads import printBWinfo

#s = xmlrpclib.ServerProxy('http://109.49.186.120:11111')

#dir_path = os.path.dirname(os.path.realpath(__file__))

print os.getcwd()


session_id = None
volunteers = []

s = xmlrpclib.ServerProxy('http://localhost:11111')

def getUsers():
    print "getting users - python"
    return s.getUsers()


#print(s.getUsers())

#Email - "Test@gmail.com"
#pw - "pw"

def signup(Email, pw):
    print "signup - python"
    return s.signup(Email, pw)

def login(Email, pw):
    print "login - python"
    session_id = s.login(Email, pw)
    return session_id

#session_id = s.login("Test@gmail.com", "pw")
#print(str(session_id))

def addMachine(session_id, machineName, CPU, Disc, RAM, price):
    print "Adding Machine - python"
    if session_id:
        return s.addMachine(session_id, machineName, CPU, Disc, RAM, price) #CPU=500MFLOPS DISC=10GB|1024MB, RAM=2GB|2048MB
    else:
        return "Login first"

def getMachine(session_id): 
    print "Getting Machines - python"
    if session_id:
        return (s.getMachine(session_id))
    else:
        return "login first"
    
    
def startVolunteer(session_id,machineName):
    print "Starting volunteer ("+machineName +") - python"
    if session_id:
    
        args = [machineName, session_id]
        p = subprocess.Popen(['python', os.path.expanduser(os.getcwd() + '/volunteer.py')] + args)
        return "Volunteer ("+machineName+") launched successfully" 
    else:
        return "Login first"

#startVolunteer("caipirinha")
#s.submitJob(session_id, 6, 2700, "NULL", "NULL", 4096, 1024)
def submitJob(session_id, price, deadline, credibility, availability, disc, RAM, RExpression):
    if session_id:
        print "Volunteers list for the job: "
        volunteers = s.submitJob(session_id, price, deadline, credibility, availability, disc, RAM)
        print volunteers
        
        if volunteers:
            chosen_one = volunteers[0]
            quiz = s.chooseVolunteer(session_id, chosen_one)
            
            ###Join quiz on expression
            RExpression = RExpression + quiz
            
            
            
            vol_ip = chosen_one["ip"]
            vol_port = chosen_one["port"]
            
            vol_conn = xmlrpclib.ServerProxy('http://'+str(vol_ip)+':'+str(vol_port))
            
            RData_file = vol_conn.compute(RExpression)
            handle = open("output.RData", "wb")
            handle.write(RData_file.data)
            handle.close()
            
            vol_conn.__close()
            return "Job executed successfully"
            
        else:
            return "No volunteers available to execute the job"
    else:
        return "Login first"

#if (volunteers):
#    bwinformation = startbandwidthScout(volunteers)
#    printBWinfo(bwinformation)

    

##try:
#   while(True):
#       time.sleep(60)

#except KeyboardInterrupt:
#   print >> pickle.sys.stderr, 'Dummy Volunteers Interrupted: "Keyboard Interrupt"'





#submitJob(session_id, preco, prazo, credibilidade, disponibilidade, disco, RAM)
#print(s.submitJob(session_id, 6, 2700, "NULL", "NULL", "4096", "1024"))




# Print list of available methods
#print(s.system.listMethods())

