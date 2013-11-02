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

"""The Betdaq API methods."""

import apimethod
import apiclient

# time in seconds to sleep between calling APIGetPrices (when called
# with > 50 market ids).
_PRICETHROTTLE = 10

# create suds clients.  There is only 1 WSDL file, but this has two
# 'services'.  The services are for 'readonly' methods and 'secure'
# methods. Secure methods use an https:// url and require the user's
# Betdaq username and password in the SOAP headers, read-only methods
# use http:// and only require username.
_rcl = apiclient.ApiClient('readonly')
_scl = apiclient.ApiClient('secure')

def set_user(name, password):
    """
    Set username and password for SOAP headers.  Note that these are
    automatically set to be const.BDAQUSER and const.BDAQPASS,
    respectively, so we only need to call this method if we don't have
    these values set.
    """
    
    _rcl.set_headers(name, password)
    _scl.set_headers(name, password)

# the Api functions appear below, first 'readonly' methods, then
# 'secure' methods, in the order that these appear in the Betdaq Api
# docs (but note that not all of the Api methods are implemented
# here).

# get all the root events e.g. 'Horse Racing', 'Soccer' etc.
ListTopLevelEvents = apimethod.ApiListTopLevelEvents(_rcl).call

# get 'subtree' and parse it for markets
GetEventSubTreeNoSelections = apimethod.\
                              ApiGetEventSubTreeNoSelections(_rcl).call

# get information for some market ids, e.g. starttime etc.
GetMarketInformation = apimethod.ApiGetMarketInformation(_rcl).call

# get prices for some market ids
GetPrices = apimethod.ApiGetPrices(_rcl, _PRICETHROTTLE).call

# get account information
GetAccountBalances = apimethod.ApiGetAccountBalances(_scl).call

# update order status
ListOrdersChangedSince = apimethod.ApiListOrdersChangedSince(_scl).call

# call ListBootstrapOrders repeatedly at startup
ListBootstrapOrders = apimethod.ApiListBootstrapOrders(_scl).call

# make order(s)
PlaceOrdersNoReceipt = apimethod.ApiPlaceOrdersNoReceipt(_scl).call

# cancel orders
CancelOrders = apimethod.ApiCancelOrders(_scl).call

# which Api services (hopefully none) am I currently blacklisted from?
ListBlacklistInformation = apimethod.\
                           ApiListBlacklistInformation(_scl).call
