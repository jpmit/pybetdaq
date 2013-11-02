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
Example of getting information on available Markets and selections on
those markets.
"""

from betdaq import api

# replace 'username' and 'password' with your credentials
api.set_user('username', 'password')

# this will return a list of 'event' objects representing Horse
# Racing, Soccer etc.
events = api.ListTopLevelEvents()

# the event ids we want markets for
eids = [e.id for e in events if e.name in ['Horse Racing', 'Rugby Union']]

# the markets for these events
markets = api.GetEventSubTreeNoSelections(eids)

# markets for which we want selection information and prices (here we
# select the first two Horse Racing markets and the last two Rugby
# Union markets - assuming that there are at least two markets for
# each of these events).
mids = [markets[i].id for i in [0,1,-1,-2]]

# after this call, selections will be a list where each item is a list
# of selection objects, each of which has price information etc.
selections = api.GetPrices(mids)
