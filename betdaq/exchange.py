# exchange.py
# James Mithen
# jamesmithen@gmail.com

"""
Event, Market, Selection and Order objects.  Also contained here are
constants for order status, such as O_UNMATCHED.
"""

import const
import exchangedata

class Event(object):
    """A top level event e.g. 'Rugby Union'."""
    def __init__(self, name, myid, **kwargs):
        # convert name to ascii string i.e. ignore any funky unicode
        # characters
        self.name = name.encode('ascii', 'ignore')
        self.id = myid

        # store all information that comes from the API
        self.properties = kwargs

    def __repr__(self):
        return ' '.join([self.name, str(self.id)])

    def __str__(self):
        return self.__repr__()

class Market(object):
    """A market."""
    def __init__(self, name, myid, pid, inrunning, **kwargs):
        # convert name to ascii string and ignore any funky unicode
        # characters
        self.name = name.encode('ascii', 'ignore')
        # from name, get event name, this is inside the first two |'s
        self.eventname =  self.name.split('|')[1]
        self.id = myid
        # parent id
        self.pid = pid
        # is the market 'in running?'
        self.inrunning = inrunning

        # store all information that comes from the API
        self.properties = kwargs

    def __repr__(self):
        return ' '.join([self.name, str(self.id)])

    def __str__(self):
        return self.__repr__()

class Selection(object):
    """A selection."""
    def __init__(self, name, sid, marketid, mback, mlay, lastmatched,
                 lastmatchedprice, lastmatchedamount, backprices,
                 layprices, src, wsn, **kwargs):

        # convert name to ascii string, i.e. ignore any funky unicode
        # characters.
        self.name = name.encode('ascii', 'ignore')        
        self.id = sid # selection id
        self.mid = marketid # market id I belong to
        self.matchedback = mback        
        self.matchedlay = mlay        
        self.lastmatched = lastmatched
        self.lastmatchedprice = lastmatchedprice
        self.lastmatchedamount = lastmatchedamount

        # selection reset count and withdrawal selection number
        self.src = src
        self.wsn = wsn

        # store all data from API
        self.properties = kwargs

        # list of prices and stakes [(p1,s1), (p2,s2) ...,]
        self.backprices = backprices
        self.layprices = layprices

    def __repr__(self):
        return ' '.join([self.name, str(self.id)])

    def __str__(self):
        return self.__repr__()
    
# BDAQ order _Status can be
# 1 - Unmatched.  Order has SOME amount available for matching.
# 2 - Matched (but not settled).
# 3 - Cancelled (at least some part of the order was unmatched).
# 4 - Settled.
# 5 - Void.
# 6 - Suspended.  At least some part unmatched but is suspended.
# here we use the same numbering scheme, but we add staus 'NOTPLACED'
# for our own internal use.
O_NOTPLACED = 0
O_UNMATCHED = 1
O_MATCHED = 2
O_CANCELLED = 3
O_SETTLED = 4
O_VOID = 5
O_SUSPENDED = 6
# polarity
O_BACK = 1
O_LAY = 2

class Order(object):
    """Returned after an order is placed."""
    def __init__(self, sid, stake, price, polarity, **kwargs):
        self.sid = sid
        self.stake = stake
        self.price = price
        self.polarity = polarity # 1 for back, 2 for lay

        # the status set here is the default and it will be
        # overwritten by the dict kwargs.
        self.status = O_NOTPLACED

        # set default values which may be overridden by **kwargs
        # selection reset count and withdrawal sequence number (needed
        # for BDAQ).
        self.src = 0
        self.wsn = 0

        # persistence type (used for betfair); default here is 'in
        # play', which means the order persists (is not cancelled)
        # when the order goes in play (e.g. when a horse race or
        # football match starts).
        self.persistence = 'IP'

        for kw in kwargs:
            # notable kwargs (and therefore possible instance attributes) are:
            # oref           - reference number from API
            # status         - one of the numbers above e.g. MATCHED
            # matchedstake   - amount of order matched
            # unmatchedstake - amount of order unmatched
            # src            - selection reset count
            # wsn            - withdrawal sequence number
            setattr(self, kw, kwargs[kw])

    def __repr__(self):
        """Note we use dollar symbol rather than GBP symbol here."""
        return '{0} {1} ${2} {3}'.format('BACK' if self.polarity == 1
                                         else 'LAY', self.sid,
                                         self.stake, self.price)

    def __str__(self):
        return self.__repr__()
