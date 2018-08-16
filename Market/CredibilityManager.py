'''
Created on 14/08/2018

@author: ricar
'''


def update_credibility(cur, con, mid, status):
    if status == "Success":
        try:
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
        if status == "Wrong":
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
            
            
        
    
    