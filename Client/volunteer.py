'''
Created on May 7, 2018

@author: ricardomaia
'''
import xmlrpclib
import sys
import threading
import os


from SimpleXMLRPCServer import SimpleXMLRPCServer

import pyRserve
import uptime


client_conn = xmlrpclib.ServerProxy('http://localhost:11111')

session_id = client_conn.checkVolunteer(sys.argv[2], sys.argv[1])

if(session_id):
    sys.exit(0)

server = SimpleXMLRPCServer(("0.0.0.0", 0), logRequests=False, allow_none=True)
server.register_introspection_functions()

listenner_port = server.server_address[1];
print "Volunteer "+ sys.argv[1] + " listenning on port: "+ str(listenner_port)

vol_session_id = client_conn.startVolunteer(sys.argv[2], listenner_port, sys.argv[1])



def RComputing(jobId, RExpression, input_binary_data):
    try:
        conn = pyRserve.connect()
    except:
        print "RServe not running... execute Rserve"
        return
    
    try:
        
        conn.eval("rm(list=ls())")
        print "R variables cleaned"
    
        ##create a RData file from the input_binary_data received from the client
        ##The file name is the path to the Rserve directory + the filename
        path = conn.eval('getwd()')
        input_filename = str(path)+"/"+str(jobId) + "_input.RData"
        
        handle = open(input_filename, "wb")
          
        #Write the bytes to the file  
        handle.write(input_binary_data.data)
        handle.close()
        
    
        #Load the RData file created previously
        # Now the volunteer has the variables and functions loaded to execute the job
        conn.voidEval('load("'+input_filename+'")')
        
        print "input RData file loaded"
         
        
        print conn.eval(str(RExpression))
        print("Expression computed")
        
        ##Save the environment with the variables updated after computing the expression
        print conn.eval('save.image("'+str(jobId)+'_output.RData")')
        print("output.RData produced")
        path = conn.eval('getwd()')
        
        output_filename = str(path)+"/"+str(jobId)+"_output.RData"
        with open(output_filename, "rb") as handle:
            output_binary_data = xmlrpclib.Binary(handle.read())
    
        print "binary_data produced"
        
        conn.close()
        if conn.isClosed:
            print "Rserve connection is closed"
            
        try:
            os.remove(output_filename)
        except OSError:
            pass
    
        try:
            os.remove(input_filename)
        except OSError:
            pass
            
    except:
    
        print "Error computing the job"
        client_conn.ExecutionError(vol_session_id, jobId)
        
    return output_binary_data


def client_compute(jobId, RExpression, input_binary_data):
            
    output_binary_data = RComputing(jobId, RExpression, input_binary_data)    
    
    client_conn.checkJobResult(vol_session_id, jobId, output_binary_data, input_binary_data)


#threadBandwidthEstimator = startBW()
def compute_job(jobId, RExpression, input_binary_data):
    
    ##Validate job
    ##Volunteer asks to market if this user can execute this job
    ##If market validate the execution then return a token of 10 computing minutes
    
    print("RExpression to compute:" + str(RExpression))
    
    t = threading.Thread(target=client_compute, args=(jobId, RExpression, input_binary_data))
    t.start()
    
    return "job was sent successfully"

server.register_function(compute_job, 'compute_job')


def healthCheck():
    
    return uptime.uptime()

server.register_function(healthCheck, 'healthCheck')

server.serve_forever()
