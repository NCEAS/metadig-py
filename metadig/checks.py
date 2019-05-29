"""Metadig check utilities
"""

import sys
import urllib2
from urlparse import urlparse

def getType(object):
    print 'type: {}'.format(type(object))
        
def isResolvable(url):
# First parse the url for a protocol, host port and path

    #url = 'https://cn.dataone.org/cn/v2/resolve/urn:uuid:7098ba54-ca6f-4e35-beb3-718bd0fe58a8'
    urlComps = urlparse(url)
    location = urlComps.netloc
    if(urlComps.netloc == ""):
        return (False, '"{}" does not appear to be a URL'.format(url))
        
    # Check the 'schema' to see if it is an open one. Currently we 
    # are just check for http and https.
    knownProtocols = ['http', 'https']
    if(urlComps.scheme not in set(knownProtocols)):
        return (False, 'Unknown or proprietary communications protocol: "{}", known protocols: {}'.format(urlComps.scheme, ", ".join(knownProtocols)))
        
    request = urllib2.Request(url)
    request.get_method = lambda : 'HEAD'
    # Python urllib2 strangly throws an error for a http status, and the response object is returned
    # by the exception code. 
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as he:
        # An error was encountered resolving the url, check which one so that we can print 
        # a more meaningful error message than provided by HTTPError
        # FYI, HTTP status codes (from FAIR FM_A1.1 https://github.com/FAIRMetrics/Metrics/blob/master/Distributions/FM_A1.1.pdf)
        if (he.code == 400):
            return (False, "Unable to resolved URL {}: Bad request".format(url))
        elif (he.code == 401):
            return (False, "Unable to resolved URL {}: Unauthorized".format(url))
        elif (he.code == 404):
            return (False, "Unable to resolved URL {}: Not Found".format(url))
        elif (he.code == 500):
            return (False, "Unable to resolved URL {}: Server Error".format(url))
        else:
            return (False, 'Error resolving URL "{}": {} {}'.format(url, he.code, he.headers))
    except urllib2.URLError as ue:
        print("URLError.reason", ue.reason)
        return (False, ue.reason[1])
    except Exception() as e:
        print("Exception: ", e)
        return (False, str(e))
    
    if(response.code in set([200, 202, 203, 206, 301, 302, 303])):
        return (True, "Successfully resolved the URL {}: status {}".format(url, response.code))
    else:
        return (False, "Successfully resolved the URL {}".format(url))

        
def getSystemMetadata(identifier, memberNode):
    # Get the DataONE system metadata for the given identifier    

    url = 'https://cn.dataone.org/cn/v2/meta/{}'.format(identifier)
        
    request = urllib2.Request(url)
    request.get_method = lambda : 'HEAD'
    # Python urllib2 strangly throws an error for a http status, and the response object is returned
    # by the exception code. 
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as he:
        # An error was encountered resolving the url, check which one so that we can print 
        # a more meaningful error message than provided by HTTPError
        # FYI, HTTP status codes (from FAIR FM_A1.1 https://github.com/FAIRMetrics/Metrics/blob/master/Distributions/FM_A1.1.pdf)
        if (he.code == 400):
            return (False, "Unable to resolved URL {}: Bad request".format(url))
        elif (he.code == 401):
            return (False, "Unable to resolved URL {}: Unauthorized".format(url))
        elif (he.code == 404):
            return (False, "Unable to resolved URL {}: Not Found".format(url))
        elif (he.code == 500):
            return (False, "Unable to resolved URL {}: Server Error".format(url))
        else:
            return (False, 'Error resolving URL "{}": {} {}'.format(url, he.code, he.headers))
    except urllib2.URLError as ue:
        print("URLError.reason", ue.reason)
        return (False, ue.reason[1])
    except Exception() as e:
        print("Exception: ", e)
        return (False, str(e))
    
    if(response.code in set([200, 202, 203, 206, 301, 302, 303])):
        return (True, "Successfully resolved the URL {}: status {}".format(url, response.code))
    else:
        return (False, "Successfully resolved the URL {}".format(url))

# Check if an identifier has a valid, known namespace
#def isNamespaceValid(identifier):
#    delimiter = ':'
#    if(identifier.find(delimeter == -1)):
#        return False, "Missing namespace in identifier"
#        
#    namespace, id = identfier.split(':', 1)
#    
#    return True, "The namespace is valid"
