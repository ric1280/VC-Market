'''
Created on May 24, 2018

@author: ricardomaia
'''


import pyRserve
import os
import xmlrpclib

conn = pyRserve.connect()

dir_path = os.path.dirname(os.path.realpath(__file__))

conn.eval("rm(list=ls())")
print conn.eval("""fibvals <- numeric(10)
            fibvals[1] <- 1
            fibvals[2] <- 1
            for (i in 3:length(fibvals)) { 
                fibvals[i] <- fibvals[i-1]+fibvals[i-2]
            } 
            
            \n collatz <- function(n, acc=0) {
                if(n==1) return(acc);
                collatz(ifelse(n%%2==0, n/2, 3*n +1), acc+1)
                }
                
                quiz<-collatz(27)
               """)
print conn.eval('save.image("output.RData")')

path = conn.eval('getwd()')

with open(str(path)+"/output.RData", "rb") as handle:
    binary_data = xmlrpclib.Binary(handle.read())
    
    
    handle = open("output.RData", "wb")
    handle.write(binary_data.data)
    print 
    
    handle.close()

