# apiclient.py
# James Mithen
# jamesmithen@gmail.com

"""
BdaqApiClient class used in calling API functions for BDAQ.
"""

from suds.client import Client
from suds.sax.element import Element
import const

class ApiClient(object):
    """
    Client object to handle requests to the API.  This simply
    configures the Client object from the Suds library.  Instances
    comes in two flavors, if __init__ is called with 'secure' we have
    a client that for calling the 'secure' API methods, if it is
    called with 'readonly' we have a client for calling the 'readonly'
    methods (see the BDAQ docs).  The difference between these two is
    that the secure client will send the password in SOAP requests,
    the readonly client will not.
    """
    
    # mapping from my names to the WSDL info
    _READONLY = 'readonly'    
    _SECURE   = 'secure'
    _sdict    = {_READONLY: ['ReadOnlyService', 0],
                 _SECURE:   ['SecureService', 1]}
    
    def __init__(self, service):
        """
        Create the SUDS client with the correct options and headers
        for the chosen service, which can be either 'readonly' or
        'secure'.
        """
        
        # allowed services
        aservices = ApiClient._sdict.keys()
        if service not in aservices:
            raise IOError('service must be one of: {0}'.\
                          format(' '.join(aservices)))
        self.service = service
        self.snum = ApiClient._sdict[self.service][1]
        # after this call, self.client will be a SUDS client object
        self._create_suds_client()

    def _create_suds_client(self):
        """Return SUDS client for BDAQ API."""
        
        self.client = Client(const.WSDLLOCAL)
        self.client.set_options(service = ApiClient._sdict[self.service][0],
                                headers = {'user-agent': const.USERAGENT})

        # put username (and password if necessary) into the headers.
        # note that another way to do this is to call betdaq.set_user,
        # so the username and password in const.py do not need to be
        # specified.
        self.set_headers(const.BDAQUSER, const.BDAQPASS)

    def method_names(self):
        """Return list of methods (API functions)"""
        
        return self.client.wsdl.services[self.snum].ports[0].methods.keys()

    def set_headers(self, name, password):
        """Set the username and password that needs to go in the SOAP header."""
           
        # this SOAP header is required by the API in this form
        header = Element('ExternalApiHeader')
        
        if self.service == ApiClient._READONLY:
            # we send the username only in the SOAP header
            astring = ('version="{0}" currency="GBP" languageCode="en" '
                       'username="{1}" '
                       'xmlns="http://www.GlobalBettingExchange'
                       '.com/ExternalAPI/"'.format(const.BDAQAPIVERSION,
                                                   name))
        if self.service == ApiClient._SECURE:
            # we send the username and password in the SOAP header
            astring = ('version="{0}" currency="GBP" languageCode="en" '
                       'username="{1}" password="{2}" '
                       'xmlns="http://www.GlobalBettingExchange'
                       '.com/ExternalAPI/"'.format(const.BDAQAPIVERSION,
                                                   name,
                                                   password))
        # set header
        header.attributes = [astring]
        self.client.set_options(soapheaders = header)
