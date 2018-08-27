'''
Created on May 24, 2018

@author: ricardomaia
'''


import pyRserve
import os
import xmlrpclib
import subprocess

list1 = [3,4,5]
for i in range(0, len(list1)):
    list1[i] = list1[i] +1
    
print list1


def RComputing():
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




try:
    conn = pyRserve.connect()
    RComputing()
except:
    print "RServe not running... starting RServe"
    dir_path = os.path.dirname(os.path.realpath(__file__))
    VC_Market_dir = dir_path + "\\..\\"
    print VC_Market_dir
    bashCommand = "Rscript "+ VC_Market_dir+"RServe_start_script.R"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    
    print "Rserve is running"
    conn = pyRserve.connect()
    RComputing()
    process.terminate()
    
    

