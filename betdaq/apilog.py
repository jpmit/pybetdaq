# apilog.py
# James Mithen
# jamesmithen@gmail.com

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
