# exchangedata.py
# James Mithen
# jamesmithen@gmail.com
#
# Some information for the exchanges, including odds ladders and
# useful functions for these.

import math
import const

# same for both BDAQ and BF
MINODDS = 1.0
MAXODDS = 1000.0

# consecutive odds for min odds (again same for both exchanges).  This
# is useful for knowing when the order book is empty.
MINODDSPLUS1 = 1.01

# Allowed odds for BDAQ data
# --------------------------
# Increments below obtained by testing betdaq.com on 4th August
# 1 	   3 	   0.01
# 3.05 	4 	   0.05
# 4.1 	6 	   0.1
# 6.2 	10 	0.2
# 10.5 	20 	0.5
# 21 	   50 	1
# 52     200   2
# 200    1000  5

# Allowed odds for BF data
# ------------------------
# Table below taken from
# http://help.betfair.info/contents/itemId/i65767327/index.en.html on
# 4th August 2013 : 
# From 	To 	Increment
# 1 	   2 	   0.01
# 2.02 	3 	   0.02
# 3.05 	4 	   0.05
# 4.1 	6 	   0.1
# 6.2 	10 	0.2
# 10.5 	20 	0.5
# 21 	   30 	1
# 32 	   50 	2
# 55 	   100 	5
# 110 	1000 	10
# 1000+ 	   Not Allowed
# The odds increment on Asian Handicap markets is 0.01 for all odds
# ranges.

def next_shorter_odds(exid, odds):
    """Return odds one shorter (i.e. less in decimal) than odds."""
    if exid == const.BDAQID:
        # use BDAQ betting increments
        if odds <= 3:
            return odds - 0.01
        elif odds <= 4:
            return odds - 0.05
        elif odds <= 6:
            return odds - 0.1
        elif odds <= 10:
            return odds - 0.2
        elif odds <= 20:
            return odds - 0.5
        elif odds <= 50:
            return odds - 1
        elif odds <= 200:
            return odds - 2
        elif odds <= 1000:
            return odds - 5

    elif exid == const.BFID:
        # use BF betting increments
        if odds <= 2 :
            return odds - 0.01
        elif odds <= 3:
            return odds - 0.02
        elif odds <= 4:
            return odds - 0.05        
        elif odds <= 6:
            return odds - 0.1
        elif odds <= 10:
            return odds - 0.2
        elif odds <= 20:
            return odds - 0.5
        elif odds <= 30:
            return odds - 1
        elif odds <= 50:
            return odds - 2
        elif odds <= 100:
            return odds - 5
        elif odds <= 1000:
            return odds - 10
    else:
        raise DataError, 'exid must be either {0} or {1}'\
              .format(const,BDAQID, const.BFID)

def next_longer_odds(exid, odds):
    """Return odds one longer (i.e. greater in decimal) than odds."""
    if exid == const.BDAQID:
        # use BDAQ betting increments
        if odds < 3 :
            return odds + 0.01
        elif odds < 4:
            return odds + 0.05
        elif odds < 6:
            return odds + 0.1
        elif odds < 10:
            return odds + 0.2
        elif odds < 20:
            return odds + 0.5
        elif odds < 50:
            return odds + 1
        elif odds < 200:
            return odds + 2
        elif odds < 1000:
            return odds + 5

    elif exid == const.BFID:
        # use BF betting increments
        if odds < 2 :
            return odds + 0.01
        elif odds < 3:
            return odds + 0.02
        elif odds < 4:
            return odds + 0.05        
        elif odds < 6:
            return odds + 0.1
        elif odds < 10:
            return odds + 0.2
        elif odds < 20:
            return odds + 0.5
        elif odds < 30:
            return odds + 1
        elif odds < 50:
            return odds + 2
        elif odds < 100:
            return odds + 5
        elif odds < 1000:
            return odds + 10

    else:
        raise DataError, 'exid must be either {0} or {1}'\
              .format(const,BDAQID, const.BFID)

def closest_longer_odds(exid, odds):
    """Return closest valid odds on exid that are equal to or longer
    (i.e. greater in decimal) than odds passed."""

    if odds < MINODDS:
        return MINODDS
    elif odds > MAXODDS:
        return MAXODDS

    # first get odds to two decimal places ROUNDED UP
    rodds = math.ceil(odds*100) / 100

    if exid == const.BDAQID:
        # use BDAQ betting increments
        if odds < 3 :
            return rodds
        elif odds < 4:
            return math.ceil(rodds/0.05)*0.05
        elif odds < 6:
            return math.ceil(rodds/0.1)*0.1
        elif odds < 10:
            return math.ceil(rodds/0.2)*0.2            
        elif odds < 20:
            return math.ceil(rodds/0.5)*0.5            
        elif odds < 50:
            return math.ceil(rodds/1.0)*1.0
        elif odds < 200:
            return math.ceil(rodds/2.0)*2.0            
        elif odds < 1000:
            return math.ceil(rodds/5.0)*5.0            

    elif exid == const.BFID:
        # use BF betting increments
        if odds < 2 :
            return rodds
        elif odds < 3:
            return math.ceil(rodds/0.02)*0.02
        elif odds < 4:
            return math.ceil(rodds/0.05)*0.05
        elif odds < 6:
            return math.ceil(rodds/0.1)*0.1
        elif odds < 10:
            return math.ceil(rodds/0.2)*0.2
        elif odds < 20:
            return math.ceil(rodds/0.5)*0.5
        elif odds < 30:
            return math.ceil(rodds/1.0)*1.0
        elif odds < 50:
            return math.ceil(rodds/2.0)*2.0
        elif odds < 100:
            return math.ceil(rodds/5.0)*5.0
        elif odds < 1000:
            return math.ceil(rodds/10.0)*10.0

def closest_shorter_odds(exid, odds):
    """Return closest valid odds on exid that are equal to or shorter
    (i.e. smaller in decimal) than odds passed."""

    if odds < MINODDS:
        return MINODDS
    elif odds > MAXODDS:
        return MAXODDS
    
    # first get odds to two decimal places ROUNDED DOWN
    rodds = math.floor(odds*100) / 100
    
    if exid == const.BDAQID:
        # use BDAQ betting increments
        if odds <= 3 :
            return rodds
        elif odds <= 4:
            return math.floor(rodds/0.05)*0.05
        elif odds <= 6:
            return math.floor(rodds/0.1)*0.1
        elif odds <= 10:
            return math.floor(rodds/0.2)*0.2            
        elif odds <= 20:
            return math.floor(rodds/0.5)*0.5            
        elif odds <= 50:
            return math.floor(rodds/1.0)*1.0
        elif odds <= 200:
            return math.floor(rodds/2.0)*2.0            
        elif odds <= 1000:
            return math.floor(rodds/5.0)*5.0            

    elif exid == const.BFID:
        # use BF betting increments
        if odds <= 2 :
            return rodds
        elif odds <= 3:
            return math.floor(rodds/0.02)*0.02
        elif odds <= 4:
            return math.floor(rodds/0.05)*0.05
        elif odds <= 6:
            return math.floor(rodds/0.1)*0.1
        elif odds <= 10:
            return math.floor(rodds/0.2)*0.2
        elif odds <= 20:
            return math.floor(rodds/0.5)*0.5
        elif odds <= 30:
            return math.floor(rodds/1.0)*1.0
        elif odds <= 50:
            return math.floor(rodds/2.0)*2.0
        elif odds <= 100:
            return math.floor(rodds/5.0)*5.0
        elif odds <= 1000:
            return math.floor(rodds/10.0)*10.0
