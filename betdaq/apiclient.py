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
        self.client = self._create_suds_client()

    def _create_suds_client(self):
        """Return SUDS client for BDAQ API."""
        
        client = Client(const.WSDLLOCAL)
        client.set_options(service = ApiClient._sdict[self.service][0],
                           headers = {'user-agent': const.USERAGENT})
        
        # this SOAP header is required by the API in this form
        header = Element('ExternalApiHeader')
        
        if self.service == ApiClient._READONLY:
            # we send the username only in the SOAP header
            astring = ('version="{0}" currency="GBP" languageCode="en" '
                       'username="{1}" '
                       'xmlns="http://www.GlobalBettingExchange'
                       '.com/ExternalAPI/"'.format(const.BDAQAPIVERSION,
                                                   const.BDAQUSER))
        if self.service == ApiClient._SECURE:
            # we send the username and password in the SOAP header
            astring = ('version="{0}" currency="GBP" languageCode="en" '
                       'username="{1}" password="{2}" '
                       'xmlns="http://www.GlobalBettingExchange'
                       '.com/ExternalAPI/"'.format(const.BDAQAPIVERSION,
                                                   const.BDAQUSER,
                                                   const.BDAQPASS))
        # set header
        header.attributes = [astring]
        client.set_options(soapheaders=header)    
        return client

    def method_names(self):
        """Return list of methods (API functions)"""
        
        return self.client.wsdl.services[self.snum].ports[0].methods.keys()
