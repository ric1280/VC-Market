'''
Created on May 24, 2018

@author: ricardomaia
'''


import pyRserve
import os
import xmlrpclib

conn = pyRserve.connect()

dir_path = os.path.dirname(os.path.realpath(__file__))

print conn.eval("a<-1+2")
print conn.eval('save.image("output.RData")')

path = conn.eval('getwd()')

with open(str(path)+"/output.RData", "rb") as handle:
    binary_data = xmlrpclib.Binary(handle.read())

