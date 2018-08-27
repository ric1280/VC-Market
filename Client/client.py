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
from _mysql import connection


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
def submitJob(session_id, price, deadline, credibility, CPU, disc, RAM, RExpression, fileName, meanUptime, RData_fileName, variables_list):
    if session_id:
        print "Volunteers list for the job: "
        jobId = s.submitJob(session_id, price, deadline, credibility, CPU, disc, RAM, fileName, meanUptime, variables_list)
        
        volunteers = s.getVolunteersForJob(session_id, jobId)
        if(volunteers=="error"):
            return "wrong jobId - you don't have owner permissions to that job"
        
        print volunteers
        
        
        if volunteers:
            
            
            chosen_one = volunteers[0]
            quiz = s.chooseVolunteer(session_id, jobId,chosen_one)
            
            ###Join quiz on expression
            
            RExpression = RExpression + quiz
            
            vol_ip = chosen_one["ip"]
            vol_port = chosen_one["port"]
            
            vol_conn = xmlrpclib.ServerProxy('http://'+str(vol_ip)+':'+str(vol_port))
            
            print "sending job to volunteer at:  "+str(vol_ip)+':'+str(vol_port)
            
            with open(RData_fileName, "rb") as handle:
                input_binary_data = xmlrpclib.Binary(handle.read())
            
            print vol_conn.compute_job(jobId, RExpression, input_binary_data)
            
            try:
                os.remove(RData_fileName)
            except OSError:
                pass
            
            return "Job dispatched successfully"
            
        else:
            s.abortJob(session_id, jobId)
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

def majorityReport(session_id, jobId, RExpression, quorum, RData_fileName):
    ## the quorum can be any odd number >= 3 
    ## For example 3, 5, 7, 9, etc.
    
    ##There is no need to submit the job because this option can only be activated to complain / validate a previous computed job
    ##So the job is already on database
    
    jobId = long(jobId)
    
    
    volunteers = s.getVolunteersForJob(session_id, jobId)
    
    print "get volunteers done"
    if(volunteers=="error"):
        return "wrong jobId - you don't have owner permissions to that job"
    
    if quorum % 2 == 0 or quorum < 3:
        return "Enter a valid quorum number: must be a odd integer number bigger or equal to 3"
        
    if len(volunteers)>= quorum-1:
        
        
        chosen_volunteers = []
        quizes = []
        
        
        with open(RData_fileName, "rb") as handle:
            input_binary_data = xmlrpclib.Binary(handle.read())
        
        for i in range(0, quorum-1):
            print "choosing volunteer"
            chosen_volunteer = volunteers[i]
            quiz = s.chooseVolunteer(session_id, jobId, chosen_volunteer)
            
            chosen_volunteers.append(chosen_volunteer)
            quizes.append(quiz)
            ###Join quiz on expression
            Expression = RExpression + quiz
    
            vol_ip = chosen_volunteer["ip"]
            vol_port = chosen_volunteer["port"]
        
            vol_conn = xmlrpclib.ServerProxy('http://'+str(vol_ip)+':'+str(vol_port))
            print "sending job to volunteer at:  "+str(vol_ip)+':'+str(vol_port)
            
            print vol_conn.compute_job(jobId, Expression, input_binary_data)
         
        
        try:
            os.remove(RData_fileName)
        except OSError:
            pass
        
        return "Job dispatched successfully"

        
        

def getJobs(session_id):
    return s.getJobs(session_id)


def loadJob(session_id, jobId):
    
    result = s.loadJob(session_id, jobId)
    if isinstance(result, basestring):
        return result
    
    handle = open(str(jobId)+"_output.RData", "wb")
        
    handle.write(result.data)
    handle.close()
    
    return "OK"
        


# Print list of available methods
#print(s.system.listMethods())

