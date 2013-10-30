# getmarkets.py
# James Mithen
# jamesmithen@gmail.com

"""
Example of getting information on available Markets and selections on
those markets.
"""

import betdaq
import exchange
from random import randint

# this will return a list of 'event' objects representing Horse
# Racing, Soccer etc.
events = betdaq.ListTopLevelEvents()

# the event ids we want markets for
eids = [e.id for e in events if e.name in ['Horse Racing', 'Rugby Union']]

# the markets for these events
markets = betdaq.GetEventSubTreeNoSelections(eids)

# markets for which we want selection information and prices (here we
# select the first two Horse Racing markets and the last two Rugby
# Union markets - assuming that there are at least two markets for
# each of these events).
mids = [markets[i].id for i in [0,1,-1,-2]]

# after this call, selections will be a list where each item is a list
# of selection objects, each of which has price information etc.
selections = betdaq.GetPrices(mids)
