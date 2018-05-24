'''
Created on May 11, 2018

@author: ricardomaia
'''
import hmac
import uuid
import time
from hashlib import sha256

import os


volunteer_sessions = dict()
session_key = os.urandom(64)
EPOCH = 1523506158



def get_timestamp():
    return int(time.time() - EPOCH)
    
def is_timestamp_expired(timestamp, max_age = 120): 
    age = get_timestamp() - timestamp
    if age > max_age:
        return True
    return False

def invalidate_volunteer_session_id(session_id):

    try:
        del volunteer_sessions[session_id]
    except KeyError:
        pass
    

def generate_volunteer_session_id(name):
    string_aux = name + str(uuid.uuid4())
   
    hmac_aux = hmac.new(session_key, string_aux, sha256)
    digest = hmac_aux.hexdigest()
    return digest

def find_volunteer_session_by_name(name):
    if volunteer_sessions:
        for session in volunteer_sessions:
            if volunteer_sessions[session]['Name'] == name:
                return volunteer_sessions[session]
    return None

def load_session(machineName):
    session = find_volunteer_session_by_name(machineName)
    if session: 
        if is_timestamp_expired(session["last_visit"]):
                invalidate_volunteer_session_id(session["session_id"])
        else:
            return session["session_id"]
   
    return None
    