'''
Created on May 7, 2018

@author: ricardomaia
'''
import xmlrpclib
import sys


from SimpleXMLRPCServer import SimpleXMLRPCServer

import pyRserve

client_conn = xmlrpclib.ServerProxy('http://localhost:11111')

session_id = client_conn.checkVolunteer(sys.argv[2], sys.argv[1])

if(session_id):
    sys.exit(0)

server = SimpleXMLRPCServer(("0.0.0.0", 0), allow_none=True)
server.register_introspection_functions()

listenner_port = server.server_address[1];
print "Volunteer "+ sys.argv[1] + " listenning on port: "+ str(listenner_port)

print(client_conn.startVolunteer(sys.argv[2], listenner_port, sys.argv[1]))

try:
    conn = pyRserve.connect()
except:
    print "RServe not running... execute Rserve"
    sys.exit(0)

#threadBandwidthEstimator = startBW()

def compute(RExpression):
    print("RExpression to compute:" + str(RExpression))
    
    conn.eval("rm(list=ls())")
    print "R variables cleaned"
    print conn.eval(str(RExpression))
    print("Expression computed")
    print conn.eval('save.image("output.RData")')
    print("output.RData produced")
    path = conn.eval('getwd()')
    
 
    with open(str(path)+"/output.RData", "rb") as handle:
        binary_data = xmlrpclib.Binary(handle.read())

    print "binary_data produced"
    return binary_data
    
server.register_function(compute, 'compute')


def healthCheck():
    return "ok"
server.register_function(healthCheck, 'healthCheck')

server.serve_forever()
