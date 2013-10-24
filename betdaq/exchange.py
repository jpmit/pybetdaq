# exchange.py
# James Mithen
# jamesmithen@gmail.com

"""Event, Market and Selection objects"""

import const
import exchangedata

class Event(object):
    """A top level event e.g. 'Rugby Union'."""
    def __init__(self, name, myid, **kwargs):
        # convert name to ascii string and ignore any funky unicode
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
    """A market"""
    def __init__(self, name, myid, pid, inrunning, pname=None):
        # convert name to ascii string and ignore any funky unicode
        # characters
        self.name = name.encode('ascii', 'ignore')
        # from name, get event name, this is inside the first two |'s
        self.eventname =  self.name.split('|')[1]
        self.id = myid
        # parent id
        self.pid = pid
        self.pname = pname
        # is the market 'in running?'
        self.inrunning = inrunning

    def __repr__(self):
        return ' '.join([self.name, str(self.id)])

    def __str__(self):
        return self.__repr__()

class Selection(object):
    """A selection"""
    def __init__(self, name, myid, marketid, mback, mlay, lastmatched,
                 lastmatchedprice, lastmatchedamount, backprices,
                 layprices, src=None, wsn=None):
        self.exid = exid
        # store everything from BDAQ API below
        # convert name to ascii string and ignore any funky unicode
        # characters
        self.name = name.encode('ascii', 'ignore')        
        self.id = myid # selection id
        self.mid = marketid # market id I belong to
        self.matchedback = mback        
        self.matchedlay = mlay        
        self.lastmatched = lastmatched
        self.lastmatchedprice = lastmatchedprice
        self.lastmatchedamount = lastmatchedamount

        # selection reset count and withdrawal selection number are
        # for BDAQ only
        self.src = src
        self.wsn = wsn

        # list of prices and stakes [(p1,s1), (p2,s2) ...,]
        self.backprices = backprices
        self.layprices = layprices

        # paded back and lay prices to const.NUMPRICES
        self.padback = self.PadPrices(backprices, const.NUMPRICES)
        self.padlay = self.PadPrices(layprices, const.NUMPRICES)

    def PadPrices(self, prices, num):
        """Pad prices so that if have fewer than num back or lay
        prices"""
        nprices = len(prices)
        if nprices == num:
            return prices
        # pad prices with None
        app = [(None, None)] * (num - nprices)
        return prices + app

    def best_back(self):
        """Return best back price, or 1.0 if no price"""
        if self.padback[0][0] is None:
            return exchangedata.MINODDS
        return max(exchangedata.MINODDS,
                   self.padback[0][0])

    def best_lay(self):
        """Return best lay price, or 1000.0 if no price"""
        if self.padlay[0][0] is None:
            return exchangedata.MINODDS
        return min(exchangedata.MAXODDS,
                   self.padlay[0][0])

    def make_best_lay(self):
        """Return price for if we wanted to make a market on selection
        and be the best price on offer to lay.  E.g. if exchange is BF
        and best lay price is 21, this will return 20"""
        
        blay = self.best_lay()

        # design option: if the best back price is 1, we could return
        # None, but instead lets return 1.
        if blay == exchangedata.MINODDS:
            return exchangedata.MINODDS

        return exchangedata.next_shorter_odds(self.exid, blay)

    def make_best_back(self):
        """Return price for if we wanted to make a market on selection
        and be the best price on offer to back E.g. if exchange is BF
        and best back price is 21, this will return 22."""

        bback = self.best_back()

        # design option: if the best lay price is 1000, we could
        # return None, but instead lets return 1000.
        if bback == exchangedata.MAXODDS:
            return exchangedata.MAXODDS

        return exchangedata.next_longer_odds(self.exid, bback)

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
    """Returned after an order is placed"""
    def __init__(self, exid, sid, stake, price, polarity, **kwargs):
        self.exid = exid
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
            # oref - reference number from API
            # status - one of the numbers above e.g. MATCHED
            # matchedstake - amount of order matched
            # unmatchedstake - amount of order unmatched
            # strategy - integer for strategy number
            #
            # NEEDED FOR PLACING BETS WITH BF BUT NOT BDAQ:
            # mid - market id
            #
            # NEEDED FOR PLACING BETS WITH BDAQ BUT NOT BF:
            # src - selection reset count
            # wsn - withdrawal sequence number
            setattr(self, kw, kwargs[kw])

    def __repr__(self):
        return '{0} {1} ${2} {3}'.format('BACK' if self.polarity == 1
                                         else 'LAY', self.sid,
                                         self.stake, self.price)

    def __str__(self):
        return self.__repr__()
