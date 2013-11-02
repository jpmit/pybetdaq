# makeorder.py
# James Mithen
# jamesmithen@gmail.com

"""
Example of making an order and cancelling an order.
"""

from betdaq import api, exchange

api.set_user('username', 'password')
    
# create an order object.  Note the selection id here is a dummy one.
# We may also want to pass kwargs 'src', 'wsn', 'cancelrunning', and
# 'cancelreset'.  These default to 0, 0, True and True respectively.
# Note 'src' (selection reset count) and 'wsn' withdrawal sequence
# number need to be set correctly.  These are stored in the selection
# objects (see the example getmarkets.py); here we are assuming that
# they are both 0, which may not be correct.
order = exchange.Order(-1,              # selection id
                       0.5,             # stake
                       990.0,           # price (odds)
                       exchange.O_BACK) # polarity (evaluates to 1)

# odict is a dictionary with keys that correspond to the order ids,
# and corresponding items that are the order objects.
odict = api.PlaceOrdersNoReceipt([order])

# here we have only one order in the dictionary
myorder = odict.values()[0]

# to cancel an order, pass the list of order object to the API
# function.
odict = api.CancelOrders([myorder])
