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
Odds ladder and some useful functions for these.  Note in principle
the odds ladder can change and so this should be obtained from the
Betdaq API (see the API docs).
"""

import math
import const

MINODDS = 1.0
MAXODDS = 1000.0

# consecutive odds for min odds (again same for both exchanges).  This
# is useful for knowing when the order book is empty.
MINODDSPLUS1 = 1.01

# Allowed odds for BDAQ data
# --------------------------
# Increments below obtained from betdaq.com on 4th August 2013
# 1 	   3 	   0.01
# 3.05 	4 	   0.05
# 4.1 	6 	   0.1
# 6.2 	10 	0.2
# 10.5 	20 	0.5
# 21 	   50 	1
# 52     200   2
# 200    1000  5

def next_shorter_odds(odds):
    """Return odds one shorter (i.e. less in decimal) than odds."""
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

def next_longer_odds(odds):
    """Return odds one longer (i.e. greater in decimal) than odds."""
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
