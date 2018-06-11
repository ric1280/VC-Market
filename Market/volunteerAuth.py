'''
Created on May 11, 2018

@author: ricardomaia
'''
import hmac
import uuid
import time
from hashlib import sha256

import os
from Client.client import session_id


volunteer_sessions = dict()
session_key = os.urandom(64)
EPOCH = 1523506158



def get_timestamp():
    return int(time.time() - EPOCH)
    
def is_timestamp_expired(timestamp, max_age = 40): 
    age = get_timestamp() - timestamp
    if age > max_age:
        return True
    return False

def clear_expired_sessions():
    """
    Clear all expired sessions
    """
    for session_id in volunteer_sessions.keys():
        last_visit = volunteer_sessions[session_id]["last_visit"]
        if is_timestamp_expired(last_visit):
            invalidate_volunteer_session_id(session_id)

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
  
def require_login(decorated_function):
    """
    Decorator that prevents access to action if not logged in.

    If the login check failed a xmlrpclib.Fault exception is raised
    """

    def wrapper(client_ip, session_id, *args, **kwargs):
        """ Decorated methods must always have self and session_id """

        # check if a valid session is available
        if session_id not in volunteer_sessions:
            clear_expired_sessions() # clean the session dict
            return 'Session ID invalid", "Call login(email, pass) to aquire a valid session'
            

        last_visit = volunteer_sessions[session_id]["last_visit"]

        # check if timestamp is valid
        if is_timestamp_expired(last_visit):
            invalidate_volunteer_session_id(session_id) # clean the session dict
            return 'Session ID invalid", "Call login(email, pass) to aquire a valid session'

        volunteer_sessions[session_id]["last_visit"] = get_timestamp()
        return decorated_function(client_ip, session_id, *args, **kwargs)

    return wrapper  

def health_check_request_pass(session_id):
    if session_id in volunteer_sessions: 
        volunteer_sessions[session_id]["last_visit"] = get_timestamp()
    
def health_check_request_fail(session_id):
    print "volunteer unreachable"
    if session_id in volunteer_sessions: 
        session = volunteer_sessions[session_id]
        if is_timestamp_expired(session["last_visit"]):
                invalidate_volunteer_session_id(session["session_id"])
                print "volunteer "+ session["Name"]+  " logged out"
    