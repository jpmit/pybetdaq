# const.py
# James Mithen
# jamesmithen@gmail.com

"""
Some constants that are useful globally.
"""

import suds
import sys
import os

# version number for this software
VERSION='0.1'

# print logging information to stdout while running code?
LOGGING = True

# number of prices to get from API
NUMPRICES = 5

# send as 'user-agent' header for all SOAP requests
USERAGENT = 'pybetman/%s Python/%s Suds/%s' %(VERSION,
                                              sys.version.split()[0],
                                              suds.__version__)

# path to local copy of WSDL file
WSDLLOCAL = 'file://{0}/wsdl/API.wsdl'.format(os.getcwd())

# BDAQ API version sent in SOAP headers
BDAQAPIVERSION = '2'

# BDAQ username and password
BDAQUSER = 'jimmybob'
BDAQPASS = '0am14th0uARTIST'
