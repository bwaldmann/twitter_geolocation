#!/usr/bin/python

"""MetaCarta Web Services Session access. Sign up at 
http://accounts.metacarta.com/ . Then:

import metacarta
lf = metacarta.LocationFinder("email@example.com", "password")
data = lf.request({'query':'Cambridge'})
print data['Locations'][0]['Name']

Explore API at http://ondemand.metacarta.com/webservices/explorer/ .

This module requires simplejson to run. You can get simplejson from
http://cheeseshop.python.org/pypi/simplejson .

For more information on this client, see:

http://ondemand.metacarta.com/?client=python
"""

__revision__ = "1.0.0" 

import urllib, urllib2
import simplejson

class InvalidAuth      (Exception):
    """Any invalid auth will throw this exception or a subclass. This 
      will catch 401 errors from the service, as well as other 
      missing auth information in the client."""
    pass 

class UsernameMissing  (InvalidAuth): 
    """If no username is passed to the initialization of the client, this
       Exception will be thrown with an informative message."""
    pass 

class PasswordMissing  (InvalidAuth): 
    """If no password is passed to the initialization of the client, this
       Exception will be thrown with an informative message."""
    pass   

class InvalidMethod    (Exception):
    """If an invalid method is sent with a request, this error will 
       be thrown on the client side."""
    pass 

class ServiceError     (Exception): 
    """If the service returns an error, this Exception will be thrown, with
       the text of the service error message."""
    pass 

class Session:
    """Base class for Session requests. At the moment, this implements all the
        actual functionality."""
    def __init__(self, username, password):
        "Initialize parameters like the hostname/server and authorization." 
      
        self.params = {
          'version':'1.0.0',
        }
        self.method = ""
        self.host = "ondemand.metacarta.com"
        self.path = "/webservices/"
        
        if not username:
            raise UsernameMissing("No username provided. Sign up at http://accounts.metacarta.com/.")
        if not password:
            raise PasswordMissing("No password provided. Sign up at http://accounts.metacarta.com/.")
        
        self.username = username
        self.password = password
        authinfo = urllib2.HTTPBasicAuthHandler()
        authinfo.add_password('MetaCarta Web Services', 
                              self.host, 
                              self.username, self.password)
        opener = urllib2.build_opener(authinfo)
        urllib2.install_opener(opener)
        self.auth = True 
    
    def request(self, params = {}):
        """Performs JSON fetch from WebService Session URL, returns object."""
        if not self.auth:
            raise InvalidAuth("No authorization information available.")
        
        if not self.method or \
               self.method not in ['QueryParser', 'search', 
                                   'LocationFinder', 'GeoTagger']:
            raise InvalidMethod("Method is not available.")
        
        params.update(self.params)
        url = "http://%s%s%s/JSON/basic" % (self.host, self.path, self.method)
        
        try:
            data = urllib2.urlopen(url, urllib.urlencode(params)).read()
        except urllib2.HTTPError, urlexception:
            if urlexception.code == 401:
                raise InvalidAuth("Invalid username/password. Did you enter " + \
                                  "your email address for your username? " + \
                                  "Did you sign up at " + \
                                  "http://accounts.metacarta.com/?") 
            else:
                raise urlexception 
        
        data_object = simplejson.loads(data)
        if data_object.has_key("error"):
            raise ServiceError(data_object['error'])
        return data_object    

class LocationFinder(Session):
    """Search for Locations using the LocationFinder."""
    def __init__(self, username="", password=""):
        Session.__init__(self, username,#!/usr/bin/python

"""MetaCarta Web Services Session access. Sign up at 
http://accounts.metacarta.com/ . Then:

import metacarta
lf = metacarta.LocationFinder("email@example.com", "password")
data = lf.request({'query':'Cambridge'})
print data['Locations'][0]['Name']

Explore API at http://ondemand.metacarta.com/webservices/explorer/ .

This module requires simplejson to run. You can get simplejson from
http://cheeseshop.python.org/pypi/simplejson .

For more information on this client, see:

http://ondemand.metacarta.com/?client=python
"""

__revision__ = "1.0.0" 

import urllib, urllib2
import simplejson

class InvalidAuth      (Exception):
    """Any invalid auth will throw this exception or a subclass. This 
      will catch 401 errors from the service, as well as other 
      missing auth information in the client."""
    pass 

class UsernameMissing  (InvalidAuth): 
    """If no username is passed to the initialization of the
