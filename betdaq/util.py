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

"""Some utility functions."""

from itertools import izip

def chunks(li, n):
    """Yield successive n-sized chunks from li."""
    
    for i in xrange(0, len(li), n):
        yield li[i:i+n]

def pairwise(iterable):
    """s -> (s0,s1), (s2,s3), (s4, s5), ..."""
    
    a = iter(iterable)
    return izip(a, a)

def unique(seq):
   """Return sequence with duplicates removed (order preserving)"""
   
   seen = {}
   result = []
   for item in seq:
       if item in seen:
           continue
       seen[item] = 1
       result.append(item)
   return result

