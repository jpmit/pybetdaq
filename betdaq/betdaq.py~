# bdaqapi.py
# James Mithen
# jamesmithen@gmail.com

# The BetDaq API functions.

import bdaqapimethod
import bdaqnonapimethod
from betman import database
from betman.api import apiclient

# any constants that we might need to modify

# time in seconds to sleep between calling APIGetPrices (when called
# with > 50 market ids).
PRICETHROTTLE = 10

# create suds clients
# There is only 1 WSDL file, but this has two 'services'.  The 
# services are for 'readonly' methods and 'secure' methods. Secure
# methods use an https:// url and send the 
# read-only
rcl = apiclient.BDAQAPIClient('readonly')
scl = apiclient.BDAQAPIClient('secure')
ncl = apiclient.BDAQnonAPIClient()

# database interface
dbman = database.DBMaster()

# get all the root events
GetTopLevelEvents = bdaqapimethod.APIListTopLevelEvents(rcl).call
# get markets will get 'subtree' and parse it for markets
GetMarkets = bdaqapimethod.APIGetEventSubTreeNoSelections(rcl, dbman).call
# selections and pricers for markets
# TODO: GetSelections does not seem to work when called for a single mid
GetSelections = bdaqapimethod.APIGetPrices(rcl, dbman, PRICETHROTTLE).call
GetSelectionsnonAPI = bdaqnonapimethod.nonAPIGetPrices(ncl, dbman).call

GetMarketInformation = bdaqapimethod.APIGetMarketInformation(rcl, dbman).call

# make order(s)
PlaceOrders = bdaqapimethod.APIPlaceOrdersNoReceipt(scl, dbman).call

# account information
GetAccountBalances = bdaqapimethod.APIGetAccountBalances(scl, dbman).call

#ListAccountPostings = bdaqapimethod.APIListAccountPostings(scl).call

# details of orders
# call ListBootstrapOrders repeatedly at startup
ListBootstrapOrders = bdaqapimethod.APIListBootstrapOrders(scl, dbman).call

ListOrdersChangedSince = bdaqapimethod.APIListOrdersChangedSince(scl, dbman).call

ListBlacklistInformation = bdaqapimethod.APIListBlacklistInformation(scl).call
