# Copyright (c) James Mithen 2013.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

"""
Some constants that are useful globally.
"""

import suds
import sys
import os

# version number for this software
VERSION = '0.1'

# print logging information to stdout while running code?  In the
# library itself, a logging message is printed each time an API
# function is called.
LOGGING = True

# maximum number of prices to get from API
NUMPRICES = 5

# send as 'user-agent' header for all SOAP requests
USERAGENT = 'pybetman/{0} python/{1} suds/{2}'.\
            format(VERSION, sys.version.split()[0], suds.__version__)

# path to local copy of WSDL file
_mypath = os.path.dirname(os.path.join(os.getcwd(), __file__))
_wsdlpath = os.path.join(_mypath, 'wsdl', 'API.wsdl')
WSDLLOCAL = 'file://{0}'.format(_wsdlpath)

# BDAQ API version sent in SOAP headers
BDAQAPIVERSION = '2'

# BDAQ username and password go here; alternatively, we can call
# betdaq.set_user.
BDAQUSER = 'username'
BDAQPASS = 'password'
