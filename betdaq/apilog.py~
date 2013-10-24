# betlog.py
# James Mithen
# jamesmithen@gmail.com
#
# Logging framework for betman library/application

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

# here we will use the INFO level for any API calls, and the lower
# DEBUG level for anything else.

betlog = logging.getLogger('betman')
betlog.setLevel(logging.DEBUG) # ignore anything below DEBUG

def _logfile_name():
    import time
    t = time.gmtime()
    name = '{0}{1}{2}'.format(str(t.tm_mday).zfill(2),
                              str(t.tm_mon).zfill(2), t.tm_year)

    return name

def _add_handlers():
    # formatter for all logging
    frmt = logging.Formatter(('%(asctime)s - %(name)s - %(levelname)s'
                              '- %(message)s'))

    # base name for logfile (todays date)
    lbasename = _logfile_name()

    # add a file handler for API calls
    fh = logging.FileHandler('{0}apicall{1}.log'.format(const.LOGDIR,
                                                        lbasename))
    fh.setLevel(logging.INFO)

    fh.setFormatter(frmt)
    # add the Handler to the logger
    betlog.addHandler(fh)

    # add a file handler for everything else
    fh2 = logging.FileHandler('{0}allinfo{1}.log'.format(const.LOGDIR,
                                                         lbasename))
    fh2.setLevel(logging.DEBUG)
    fh2.setFormatter(frmt)
    # add the Handler to the logger
    betlog.addHandler(fh2)

    # output everything to stdout
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(frmt)
    betlog.addHandler(ch)

if not betlog.handlers:
    _add_handlers()

# You can now start issuing logging statements in your code
#lgr.debug('debug message') # This won't print to myapp.log
#lgr.info('info message') # Neither will this.
#lgr.warn('Checkout this warning.') # This will show up in the log file.
#lgr.error('An error goes here.') # and so will this.
#lgr.critical('Something critical happened.') # and this one too.
