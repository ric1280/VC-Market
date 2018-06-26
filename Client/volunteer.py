'''
Created on May 7, 2018

@author: ricardomaia
'''
import xmlrpclib
import sys
import threading


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



def compute(jobId, RExpression):
    try:
        conn = pyRserve.connect()
    except:
        print "RServe not running... execute Rserve"
        return
    
    
    
    conn.eval("rm(list=ls())")
    print "R variables cleaned"
    print conn.eval(str(RExpression))
    print("Expression computed")
    print conn.eval('save.image("'+str(jobId)+'_output.RData")')
    print("output.RData produced")
    path = conn.eval('getwd()')
    
 
    with open(str(path)+"/"+str(jobId)+"_output.RData", "rb") as handle:
        binary_data = xmlrpclib.Binary(handle.read())

    print "binary_data produced"
    
    conn.close()
    if conn.isClosed:
        print "Rserve connection is closed"
        
    client_conn.checkJobResult(vol_session_id, jobId, binary_data)
        
    

#threadBandwidthEstimator = startBW()
def compute_job(jobId, RExpression):
    print("RExpression to compute:" + str(RExpression))
    
    t = threading.Thread(target=compute, args=(jobId, RExpression))
    t.start()
    
    return "job was sent successfully"

server.register_function(compute_job, 'compute_job')


def healthCheck():
    
    return uptime.uptime()

server.register_function(healthCheck, 'healthCheck')

server.serve_forever()
