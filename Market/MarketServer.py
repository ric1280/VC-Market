'''
Created on 28/03/2018

@author: ricar
'''


import xmlrpclib
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

import socket
import MySQLdb as mdb
import sys
import os
import datetime


import clientAuth
import volunteerAuth
import threading
from Client.client import session_id

import pyRserve
import time
from fileinput import filename
from uptime import uptime

#print(str(socket.gethostbyname(socket.getfqdn())))

jobBuffer = dict()

print "Strarting MarketServer"

try:
    con = mdb.connect('localhost', 'user', '1234', 'vcsystem');

    cur = con.cursor()
 
        
    cur.execute("SELECT VERSION()")
    ver = cur.fetchone()
    print ("Database version : %s " % ver)
    
except mdb.Error as e:
  
    print ("Error %d: %s" % (e.args[0],e.args[1]))
    sys.exit(1)


class HackyRequestHandler(SimpleXMLRPCRequestHandler):
    #def __init__(self, req, addr, server):
    #    self.client_ip, self.client_port = addr
    #    SimpleXMLRPCRequestHandler.__init__(self, req, addr, server)
    def decode_request_content(self, data):
        data = SimpleXMLRPCRequestHandler.decode_request_content(self, data)
        from xml.dom.minidom import parseString
        doc = parseString(data)
        ps = doc.getElementsByTagName('params')[0]
        pdoc = parseString(
            ''' <param><value>
                <string>%s</string>
                </value></param>''' % (self.client_address[0],))
        p = pdoc.firstChild.cloneNode(True)
        ps.insertBefore(p, ps.firstChild)
        return doc.toxml()


# Create server
server = SimpleXMLRPCServer(("0.0.0.0", 11111), requestHandler=HackyRequestHandler, allow_none=True)
server.register_introspection_functions()

# Register pow() function; this will use the value of
# pow.__name__ as the name, which is just 'pow'.
#server.register_function(pow)

# Register a function under a different name

def regist_user(client_ip, email, password):
        #Check if user already exists
        try:
            cur.execute("""SELECT * FROM Users WHERE Email='%s'""" % email)
            if cur.fetchone() != None:
                return "User already exists!"
        except:
            return "Wrong sql query!"
        
        print("registing user: " + email + " with password: " + password)
        try:
            cur.execute("""INSERT INTO Users(Email, Password, Credits) VALUES (%s, %s, %s)""", (email, password, int(500)))
            con.commit()
        except: 
            con.rollback()
        return "User registed successfully!"
        
server.register_function(regist_user, 'signup')





def login(client_ip, email, password):
 
    cur.execute("""SELECT Password FROM Users WHERE Email='%s'""" % email)
    
    result = cur.fetchone()
    if result == None:
        return "The email does not exists"    
       
    if result[0] == password:  
        return clientAuth.load_session(email)
        
    return "Wrong password, try again!"
server.register_function(login, 'login')

def getUsers(client_ip):
    print(client_ip)
    cur.execute("""SELECT * FROM Users""")
    users = cur.fetchall()
    print (str(users))
    return str(users)

server.register_function(getUsers, 'getUsers')

@clientAuth.require_login
def addMachine(client_ip,session_id, Name, CPU, Disc, RAM, Price):
    
  
    Email = clientAuth.session_to_email(session_id)
    if not Email:
        return "Wrong session_id, please login again!"
    
    try:
        cur.execute("""Select * from UserMachines INNER JOIN Machines ON UserMachines.mid=Machines.mid WHERE UserMachines.Email='%s' AND Machines.NAME='%s'""" % (Email, Name))
        if cur.fetchone() != None:
            return "Machine already exists!"
    except:
        return "Machine is already registed!"
    
    try:
        cur.execute("""SELECT COUNT(NAME) FROM Machines""")
        mid = int(cur.fetchone()[0]) + 1
        
    except:
        return "Wrong sql query!"    
    
    try:
        #scj -> successful computed jobs - for mathematical purpose starts with 1
        scj = 1
        
        #credibility is calculated by this formula Cr(mid) = 1 - (f/scj ) which f is the fraction of saboteurs in the system = 0.012 = 1.2%
        f = 0.012
        credibility = 1 - (f/scj)
        cur.execute("""INSERT INTO Machines(mid, Name, CPU, Disc, RAM, Price, scj, credibility) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (mid, Name, CPU, Disc, RAM, Price, scj, credibility))
        con.commit()
    except: 
        con.rollback()   
    
    try:
        cur.execute("""INSERT INTO UserMachines(Email, mid) VALUES (%s ,%s)""", (Email, mid))
        con.commit()
    except: 
        con.rollback()
        
    
    return ("Machine added successfully!")

server.register_function(addMachine, 'addMachine')

@clientAuth.require_login
def getMachine(client_ip, session_id):
    Email = clientAuth.session_to_email(session_id)
    
    try:
        cur.execute("""Select * from UserMachines INNER JOIN Machines ON UserMachines.mid=Machines.mid WHERE UserMachines.Email='%s'""" % (Email))
        return str(cur.fetchall()) 
    except:
        return "Error getting the machines!"
    
server.register_function(getMachine, 'getMachine')

@clientAuth.require_login
def submitJob(client_ip, session_id, price, deadline, credibility, CPU, disc, RAM, fileName):
    
    jobId=1
    try:
        cur.execute("""SELECT COUNT(jobId) FROM job""")
        jobId = int(cur.fetchone()[0]) + 1
        
    except:
        return "Wrong sql query: SELECT COUNT(jobId) FROM job!"    
    
    try:
        initTime = time.time()
        cur.execute("""INSERT INTO Job(jobId, credibility, CPU, Disc, RAM, ExecTime, Status, Price, Deadline, InitTime, file) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (jobId, credibility, CPU, disc, RAM, 0, "NULL", price, deadline, initTime, fileName))
        con.commit()
    
    except: 
        print "Could not insert job data into DB"
        con.rollback()
    
    
    try:
        cur.execute("""INSERT INTO client_job(Email, jobId) VALUES (%s ,%s)""", (clientAuth.sessions[session_id]['email'], jobId))
        con.commit()
    except: 
        con.rollback()
     

    return jobId

server.register_function(submitJob, 'submitJob')

@clientAuth.require_login
def abortJob(client_ip, session_id, jobId):
    
    try:
        query = "DELETE FROM client_job WHERE Email='"+clientAuth.sessions[session_id]['email']+"' AND jobId="+str(jobId)
        cur.execute(query)
        con.commit()
    except: 
        con.rollback()
     
    try: 
        query = "DELETE FROM job WHERE jobId="+str(jobId)
        cur.execute(query)
        con.commit()
    except: 
        con.rollback()
    
    return 
    
server.register_function(abortJob, 'abortJob')

 
def checkClientOwnership(session_id, jobId):    
    #Job owner's email
    Email = clientAuth.session_to_email(session_id)
    
    #Validate if the client is owner of job
    query = "Select jobId FROM client_job WHERE Email='"+str(Email)+"'"
    try:
        cur.execute(query)
        jobIds = cur.fetchall()
        
    except:
        return "Wrong sql query: "+ query    
    
    #Check if the user has registered this job
    jobMatching = False
    for job in jobIds:
        if jobId in job:
            jobMatching = True
            
    if not jobMatching:
        return "error"
    
    return "OK"   

@clientAuth.require_login
def getVolunteersForJob(client_ip, session_id, jobId):      
    
    valuemsg = checkClientOwnership(session_id, jobId)
    if(valuemsg != "OK"):
        return valuemsg
    
    query = "SELECT * FROM job WHERE jobId="+str(jobId)
    try:
        cur.execute(query)
        jobData = cur.fetchone()
        
    except:
        return "Wrong sql query: "+ query    
    

    price = jobData[7];
    deadline = jobData[8];
    credibility = jobData[1];
    CPU = jobData[2];
    disc = jobData[3];
    RAM = jobData[4];
    
    Email = clientAuth.session_to_email(session_id)
    
    jobBuffer[Email] = {"price"  : price,
                        "deadline": deadline,
                        "credibility": credibility,
                        "CPU": CPU,
                        "disc": disc,
                        "RAM": RAM}
    
    
    job_candidates = []
    if volunteerAuth.volunteer_sessions:
        for session in volunteerAuth.volunteer_sessions:
            machine = volunteerAuth.volunteer_sessions[session]
            
            if machine['State'] == "BUSY":
                continue
            
            if price != "NULL":
                if machine['Price'] > price:
                    continue
            if disc != "NULL":
                if machine['Disc'] < disc:
                    continue
            if RAM != "NULL":
                if machine['RAM'] < RAM:
                    continue
                
            if CPU != "NULL":
                if machine['CPU'] < CPU:
                    continue
                
            job_candidates.append({"Name"  : machine["Name"],
                                   "mid" : machine["mid"],
                                  "ip"  : machine["ip"],
                                  "port"  : machine["port"],
                                  "CPU"  : machine["CPU"],
                                  "Disc"  : machine["Disc"],
                                  "RAM"  : machine["RAM"],
                                  "Price"  : machine["Price"]})
            
    return job_candidates
   
server.register_function(getVolunteersForJob, 'getVolunteersForJob')    




#def job_result_validation(volunteer_ip, vol_session_id, jobId, ):

@clientAuth.require_login
def chooseVolunteer(client_ip, session_id, jobId, volunteer):
    #validate jobID
    valuemsg = checkClientOwnership(session_id, jobId)
    if(valuemsg != "OK"):
        return valuemsg
    #link the job to volunteer on database
    try:
        cur.execute("""INSERT INTO machine_job(mid, jobId) VALUES (%s ,%s)""", (volunteer["mid"], jobId))
        con.commit()
    except: 
        con.rollback()
        
    #update volunteer state to busy
    if volunteerAuth.volunteer_sessions:
        for session in volunteerAuth.volunteer_sessions:
            machine = volunteerAuth.volunteer_sessions[session]
            
            if machine["mid"]==volunteer["mid"]:
                machine["State"] = "BUSY"
    
    quiz = """\n collatz <- function(n, acc=0) {
                if(n==1) return(acc);
                collatz(ifelse(n%%2==0, n/2, 3*n +1), acc+1)
                }
                
                quiz<-collatz(27)
               """
    
    return quiz
    
server.register_function(chooseVolunteer, 'chooseVolunteer')    

@clientAuth.require_login
def checkVolunteer(client_ip, session_id, machineName):
    return volunteerAuth.load_session(machineName)
   
server.register_function(checkVolunteer, 'checkVolunteer')

@clientAuth.require_login
def startVolunteer(client_ip, session_id, port, machineName):
    #Check if machineName is registered by the user that corresponds to session_id 
    if session_id in clientAuth.sessions:
        Email = clientAuth.sessions[session_id]["email"]
    else: 
        return "Your login session is not valid, login again!"
    
    try:
        cur.execute("""Select Name from UserMachines INNER JOIN Machines ON UserMachines.mid=Machines.mid WHERE UserMachines.Email='%s'""" % (Email))
        machineNames = cur.fetchall()
        print (str(machineNames)) 
    except:
        return "Error getting the machines!"
    
    ##Check if machine name is registered on database
    mName_isValid = False
    for mName in machineNames:
        if machineName in mName:
            mName_isValid = True
            break
        
    
    if mName_isValid:
        
        vol_session_id = volunteerAuth.load_session(machineName)
        if vol_session_id:
            return vol_session_id
    
        # generate session id and save it    
        vol_session_id = volunteerAuth.generate_volunteer_session_id(machineName)
            
        #populate_machine_data
        try:
            cur.execute("""Select CPU, Disc, RAM, Price, Machines.mid from UserMachines INNER JOIN Machines ON UserMachines.mid=Machines.mid WHERE UserMachines.Email='%s' AND Machines.NAME='%s'""" % (Email, machineName))
            data = cur.fetchall()      
            data = data[0]
            print (str(data)) 
        except:
            return "Error getting the machines!"
    
    
        volunteerAuth.volunteer_sessions[vol_session_id] = {"Name"  : machineName,
                                                            "mid" : data[4], 
                                                          "ip"  : client_ip,
                                                          "port"  : port,
                                                          "session_id": vol_session_id,
                                                          "CPU"  : data[0],
                                                          "Disc"  : data[1],
                                                          "RAM"  : data[2],
                                                          "Price"  : data[3],
                                                          "last_visit": volunteerAuth.get_timestamp(),
                                                          "State" : "FREE",
                                                          "initTime": time.time()}
    
    
    else:
        return "wrong machine name - regist machine first"
    
    
    
    return vol_session_id

server.register_function(startVolunteer, 'startVolunteer')

@volunteerAuth.require_login
def checkJobResult(client_ip ,volunteer_session, jobId, RData_file):
    #connect to R
    try:
        conn = pyRserve.connect()
    except:
        print "RServe not running... execute Rserve"
        return

    path = conn.eval('getwd()')
    filename = str(path)+"/"+str(jobId) + "_output.RData"
    handle = open(filename, "wb")
        
    handle.write(RData_file.data)
    handle.close()

    conn.eval("rm(list=ls())")
    conn.voidEval('load("'+filename+'")')
    quiz = conn.eval("quiz")
    
    #FIT IT - check the quiz result for that job - the quiz is not always the same
    if quiz == 111:
        print "The computed job with the id "+ str(jobId) + " was successfully validated!"
        try:
            query = "UPDATE job SET Status = 'Success' WHERE jobId = "+ str(jobId)
            cur.execute(query)
            con.commit()
        
        except: 
            print "Could not execute query: "+ query
            con.rollback()
    
    
        try:
            query = """SELECT InitTime FROM job WHERE jobId= """+str(jobId)
            cur.execute(query)
            initTime = cur.fetchone()[0]
            
        except:
            print "error with query: "+query
    
        try:
            execTime = time.time() - initTime        
            query = "UPDATE job SET ExecTime = "+ str(execTime)+" WHERE jobId = "+ str(jobId)
            cur.execute(query)
            con.commit()
        
        except: 
            print "Could not execute query: "+ query
            con.rollback()
            
            
        try:
            #get successful computed jobs for that machine
            mid = volunteerAuth.volunteer_sessions[volunteer_session]["mid"]
            query = """SELECT scj FROM machines WHERE mid= """+str(mid)
            cur.execute(query)
            scj = cur.fetchone()[0]
            
            #This volunteer computed one more job successfully 
            scj = scj + 1
            f = 0.012
            credibility = 1 - (f/scj)
            
            #Update credibility and scj
            
                   
            query = "UPDATE machines SET scj = "+ str(scj)+", credibility = "+str(credibility)+" WHERE mid = "+ str(mid)
            cur.execute(query)
            con.commit()
        
        except: 
            print "Could not execute query: "+ query
            con.rollback()
        
    else: 
        #the volunteer computed a wrong result
        # scj is now set to 1
        # credibility is updated with the new scj
        
        try:
            scj = 1
            f = 0.012
            credibility = 1 - (f/scj)
            
            #Update credibility and scj
                
            query = "UPDATE machines SET scj = "+ str(scj)+", credibility = "+str(credibility)+" WHERE mid = "+ str(mid)
            cur.execute(query)
            con.commit()
        
        except: 
            print "Could not execute query: "+ query
            con.rollback()
        
        
    conn.close()
    if conn.isClosed:
        print "Rserve connection is closed"
        
    
    #Store Rdata path
    
    try:
        query = "UPDATE job SET RDataPath = '"+ str(filename)+"' WHERE jobId = "+ str(jobId)
        cur.execute(query)
        con.commit()
        
    except:
        print "Could not execute query: "+ query
        con.rollback()
    
    #update volunteer state to FREE
    volunteerAuth.volunteer_sessions[volunteer_session]["State"] = "FREE"
     
 #   try:
 #       os.remove(filename)
 #   except OSError:
 #       pass
    
    ##remove output.RData
server.register_function(checkJobResult, 'checkJobResult')

@clientAuth.require_login
def getJobs(client_ip, session_id):

    try:
        query = """Select job.jobId, job.file, job.InitTime from client_job INNER JOIN job ON client_job.jobId=job.jobId WHERE client_job.Email='%s' """ % (clientAuth.sessions[session_id]["email"])
        cur.execute(query)
        result = cur.fetchall()
    except:
         print "Could not execute query: "+ query 
        
    
    job_list = []
    for entry in result:  
        jobId = entry[0]     
        file = entry[1]
        date = datetime.datetime.fromtimestamp(entry[2]).strftime('%Y-%m-%d %H:%M:%S')
        
        job = (jobId, file, date)
        job_list.append(job)
        
    return job_list    
        
server.register_function(getJobs, 'getJobs')


@clientAuth.require_login
def loadJob(client_ip, session_id, jobId):
    
    if checkClientOwnership(session_id, jobId) != "OK":
        return "This client is not the owner of this jobId - execute getJobs() to get a list of authorized jobs"
    
    
    try:
        query = """Select job.RDataPath from client_job INNER JOIN job ON client_job.jobId=job.jobId WHERE client_job.Email='%s' AND job.jobId=%s""" % (clientAuth.sessions[session_id]["email"], jobId)
        cur.execute(query)
        path = cur.fetchone()[0]
        if not path:
            return "This client is not the owner of this jobId "
    except:
        return "Could not execute query: "+ query 
         
    with open(path, "rb") as handle:
        binary_data = xmlrpclib.Binary(handle.read())  
    
    return binary_data
        
server.register_function(loadJob, 'loadJob')        

def healthCheck():
    threading.Timer(30.0, healthCheck).start()
    print "Health-Checking Volunteers..."
    for session_id in volunteerAuth.volunteer_sessions.keys():
        vol_address = 'http://'+volunteerAuth.volunteer_sessions[session_id]["ip"]+':'+str(volunteerAuth.volunteer_sessions[session_id]["port"])
        print vol_address
        
        try:
            vol_conn = xmlrpclib.ServerProxy(vol_address)
            hc = vol_conn.healthCheck()
            
            if(hc):
                volunteerAuth.health_check_request_pass(volunteerAuth.volunteer_sessions[session_id]["session_id"])
                print "volunteer " + volunteerAuth.volunteer_sessions[session_id]["Name"] + "passed health-check successfully! - uptime -> "+str(hc)
        
        except:
            initTime = volunteerAuth.volunteer_sessions[session_id]["initTime"]
            mid = volunteerAuth.volunteer_sessions[session_id]["mid"]
            if(volunteerAuth.health_check_request_fail(volunteerAuth.volunteer_sessions[session_id]["session_id"])):
                
                
                try:
                    query = """INSERT INTO availability(mid, uptime) VALUES (%s, %s)""" % (mid, time.time()-initTime)
      
                    cur.execute(query)
                    con.commit()
            
                except:
                    print "Could not execute query: "+ query
                    con.rollback()
    
                
        

  
healthCheck()

server.serve_forever()
