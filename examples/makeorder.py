# makeorder.py
# James Mithen
# jamesmithen@gmail.com

"""
Example of making an order on Betdaq.
"""

import betdaq

order = exchange.Order(16375160,        # selection id
                       0.5,             # stake
                       10.0,            # price (odds)
                       exchange.O_BACK) # polarity
                       

betdaq.PlaceOrdersNoReceipt([order])
