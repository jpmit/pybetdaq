# makeorder.py
# James Mithen
# jamesmithen@gmail.com

"""
Example of making an order on Betdaq.
"""

import betdaq
import exchange

order = exchange.Order(17676142,        # selection id
                       0.5,             # stake
                       100.0,           # price (odds)
                       exchange.O_BACK) # polarity
                       
# odict is a dictionary with keys that correspond to the order ids,
# and corresponding items that are the order objects.
odict = betdaq.PlaceOrdersNoReceipt([order])

# here we have only one order in the dictionary
myorder = odict.values()[0]

# to cancel an order, pass the list of order object to the API
# function.
odict = betdaq.CancelOrders([myorder])
