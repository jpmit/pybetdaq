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
Logging for API calls using standard Python logging library. Here the
 INFO level is used for any API calls, and this is fed to stdout.
"""

import sys
import logging
import const

# recall the default logging priorities are
# CRITICAL = 50
# ERROR = 40
# WARNING = 30
# INFO = 20
# DEBUG = 10
# NOTSET = 0

apilog = logging.getLogger('pybetdaq')
apilog.setLevel(logging.DEBUG) # ignore anything below DEBUG

def _add_handlers():
    # formatter for all logging
    frmt = logging.Formatter(('%(asctime)s - %(name)s - %(levelname)s'
                              '- %(message)s'))

    # output everything to stdout
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(frmt)
    apilog.addHandler(ch)

if const.LOGGING and not apilog.handlers:
    _add_handlers()
