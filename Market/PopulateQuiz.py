'''
Created on 09/07/2018

@author: ricar
'''

import MySQLdb as mdb
import sys
import random
import pyRserve



try:
    con = mdb.connect('localhost', 'user', '1234', 'vcsystem');

    cur = con.cursor()
 
        
    cur.execute("SELECT VERSION()")
    ver = cur.fetchone()
    print ("Database version : %s " % ver)
    
except mdb.Error as e:
  
    print ("Error %d: %s" % (e.args[0],e.args[1]))
    sys.exit(1)

def compute(input):
    try:
        conn = pyRserve.connect()
    except:
        print "RServe not running... execute Rserve"
        return
    
    quiz = """\n collatz <- function(n, acc=0) {
                if(n==1) return(acc);
                collatz(ifelse(n%%2==0, n/2, 3*n +1), acc+1)
                }
                
                quiz<-collatz("""+str(input)+")"
                
    print "computing collatz("+str(input)+")"
               
    output = conn.eval(quiz)
    
    conn.close()
    return output


def populate(amount):
    
   
    for x in range(amount):
        input = random.randint(20,100000)
        
        output = compute(input) 
        store_quiz(input, output)
        
     


def store_quiz ( input , output):
    try:
        cur.execute("""Select * from market_quiz Where input='%s'""" % (input))
        result = cur.fetchone()
    except:
        return "Error getting quiz"
    
    
    if result == None:
        try:
            cur.execute("""insert into market_quiz(input, output) values (%s ,%s)""", (input, output))
            con.commit()
        except: 
            con.rollback()
    else:
        try:
            query = "UPDATE market_quiz SET output = "+str(output)+" WHERE input = "+ str(input)
            cur.execute(query)
            con.commit()
        
        except: 
            print "Could not execute query: "+ query
            con.rollback()

populate(100)