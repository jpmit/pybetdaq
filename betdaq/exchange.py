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
        self.id = sid       # selection id
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
# polarity of order
O_BACK = 1
O_LAY = 2

class Order(object):
    """Used to place an order, and returned after an order is placed."""
    
    def __init__(self, sid, stake, price, polarity, **kwargs):
        """
        Create order from selection id, stake (in GBP), price (odds),
        polarity (O_BACK or O_LAY).
        """
        
        self.sid = sid
        self.stake = stake
        self.price = price
        self.polarity = polarity # 1 for back, 2 for lay

        # the following are defaults and can be overridden by **kwargs
        self.status = O_NOTPLACED
        # cancel when market goes 'in running'?
        self.cancelrunning = True
        # cancel if selection is reset?
        self.cancelreset = True
        # selection reset count        
        self.src = 0
        # withdrawal selection number        
        self.wsn = 0              

        for kw in kwargs:
            # notable kwargs (and therefore possible instance attributes) are:
            # not set at instantiation:
            # oref           - reference number from API
            # matchedstake   - amount of order matched
            # unmatchedstake - amount of order unmatched
            # set at instantiation:
            # status         - one of the numbers above e.g. O_MATCHED
            # cancelrunning  - default is True
            # cancelreset    - default is True
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
