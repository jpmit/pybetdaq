# apiexception.py
# James Mithen
# jamesmithen@gmail.com

"""
Exception classes for the entire code.  These are empty at the moment
so are purely here for the descriptive names only.
"""

# base class for everything
class BetmanError(Exception): pass

class DataError(BetmanError): pass

class ApiError(BetmanError): pass
