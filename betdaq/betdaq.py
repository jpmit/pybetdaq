# bdaqapi.py
# James Mithen
# jamesmithen@gmail.com

"""The Betdaq API methods."""

import apimethod
import apiclient

# time in seconds to sleep between calling APIGetPrices (when called
# with > 50 market ids).
PRICETHROTTLE = 10

# create suds clients.  There is only 1 WSDL file, but this has two
# 'services'.  The services are for 'readonly' methods and 'secure'
# methods. Secure methods use an https:// url and require the user's
# Betdaq username and password in the SOAP headers, read-only methods use http://
# and only require username.
rcl = apiclient.ApiClient('readonly')
scl = apiclient.ApiClient('secure')

# get all the root events e.g. 'Horse Racing', 'Soccer' etc.
ListTopLevelEvents = apimethod.ApiListTopLevelEvents(rcl).call

# get 'subtree' and parse it for markets
GetEventSubTreeNoSelections = apimethod.\
                              ApiGetEventSubTreeNoSelections(rcl).call

# get prices for some market ids
GetPrices = apimethod.ApiGetPrices(rcl, PRICETHROTTLE).call

# get information for some market ids, e.g. starttime etc.
GetMarketInformation = apimethod.ApiGetMarketInformation(rcl).call

# make order(s)
PlaceOrdersNoReceipt = apimethod.ApiPlaceOrdersNoReceipt(scl).call

# get account information
GetAccountBalances = apimethod.ApiGetAccountBalances(scl).call

# call ListBootstrapOrders repeatedly at startup
ListBootstrapOrders = apimethod.ApiListBootstrapOrders(scl).call

# update order status
ListOrdersChangedSince = apimethod.ApiListOrdersChangedSince(scl).call

# which Api services (hopefully none) am I currently blacklisted from?
ListBlacklistInformation = apimethod.\
                           ApiListBlacklistInformation(scl).call
