'''
Created on May 11, 2018

@author: ricardomaia
'''
import hmac
import uuid
import time
from hashlib import sha256

import os


sessions = dict()
session_key = os.urandom(64)
EPOCH = 1523506158



def get_timestamp():
    return int(time.time() - EPOCH)
    
    
### A user is active during 900 seconds (15 minutes) without making any request to the market Server
def is_timestamp_expired(timestamp, max_age = 900): 
    age = get_timestamp() - timestamp
    if age > max_age:
        return True
    return False

def find_session_by_email(email):
    if sessions:
        for session in sessions:
            if sessions[session]['email'] == email:
                return sessions[session]
    return None
    
def invalidate_session_id(session_id):

    try:
        del sessions[session_id]
    except KeyError:
        pass
    
def clear_expired_sessions():
    """
    Clear all expired sessions
    """
    for session_id in sessions.keys():
        last_visit = sessions[session_id]["last_visit"]
        if is_timestamp_expired(last_visit):
            invalidate_session_id(session_id)


def generate_session_id(email):
    string_aux = email + str(uuid.uuid4())
   
    hmac_aux = hmac.new(session_key, string_aux, sha256)
    digest = hmac_aux.hexdigest()
    return digest
   
def require_login(decorated_function):
    """
    Decorator that prevents access to action if not logged in.

    If the login check failed a xmlrpclib.Fault exception is raised
    """

    def wrapper(client_ip, session_id, *args, **kwargs):
        """ Decorated methods must always have self and session_id """

        # check if a valid session is available
        if session_id not in sessions:
            clear_expired_sessions() # clean the session dict
            return 'Session ID invalid", "Call login(email, pass) to aquire a valid session'
            

        last_visit = sessions[session_id]["last_visit"]

        # check if timestamp is valid
        if is_timestamp_expired(last_visit):
            invalidate_session_id(session_id) # clean the session dict
            return 'Session ID invalid", "Call login(email, pass) to aquire a valid session'

        sessions[session_id]["last_visit"] = get_timestamp()
        return decorated_function(client_ip, session_id, *args, **kwargs)

    return wrapper

def session_to_email(session_id):
    return sessions[session_id]["email"]

def load_session(email):
    session = find_session_by_email(email)
    if session: 
        if is_timestamp_expired(session["last_visit"]):
                invalidate_session_id(session["session_id"])
        else:
            return session["session_id"]
    # generate session id and save it
    session_id = generate_session_id(email)
    sessions[session_id] = {"email"  : email,
                            "session_id": session_id,
                            "last_visit": get_timestamp()}
    
    return session_id  