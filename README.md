PyBetdaq
========

Copyright (c) James Mithen 2013.

PyBetdaq is an interface to the Betdaq sports exchange
(www.betdaq.com) API written in Python.  This allows trading
applications that place orders on the Betdaq exchange to be built in
Python.

The software is supplied here under the terms of the GNU GPL license,
version 3.  A copy of this license is included along with the source
code, see 'gpl.txt'.  Note that the copyright holder accepts no
responsibility for any financial loss resulting from the use of this
software.
 
In order to use PyBetdaq, you will need (i) a Betdaq account and (ii)
to be subscribed to the Betdaq API.  For more information about this,
see [api.betdaq.com](http://api.betdaq.com).  For more information
about the PyBetdaq library, read on.

REQUIREMENTS
-------------

* Python 2.x (tested with Python 2.7)
* SUDS library (see https://fedorahosted.org/suds/)

USING THE LIBRARY
-----------------

The library code, which is all written in Python, is contained in the
betdaq/ directory.  To follow along with these examples, add the path
to the parent directory of betdaq/ to your PYTHONPATH environment
variable.

The library can be used in a Python program as follows:
```python
from betdaq import api
api.set_user('username', 'password')
```

where 'username' and 'password' are for your Betdaq account.  set_user
must be called before using the api functions since the username and
password are needed in the SOAP headers (see the API docs).  As an
alternative, the username and password can be hard coded into const.py
as BDAQUSER and BDAQPASS (see const.py).

The Betdaq API functions are available in the betdaq.api namespace in
MixedCase (as in the API docs).  For example, after the above code
snippet we can write:

```python
api.ListTopLevelEvents()
```
which will return a list of Event objects, each representing a top
level event e.g. 'Horse Racing' or 'Soccer'.

As well as 'Event' objects in the example above, the library defines
'Market', 'Selection' and 'Order' objects, which are designed to be
useful abstractions for trading applications.  The library functions
typically return lists of these objects.  For example:
```python
api.GetEventSubTreeNoSelections([100004])
```
will return a list of Market objects for the top level event with id
100004 (which happens to be Horse Racing).  And:
```python
api.GetPrices([111, 112])
```

where 111 and 112 are market ids (which do not correspond to real
market ids in this example) will return a list of length 2 -
[[sel111_1, sel111_2, ...], [sel112_1, sel112_2, ...]] - where each
list item is a list of selection objects (the first item is a list of
selection objects for the market with id 111, the second item the same
for market id 112).

Further examples of how to use the library functions are given in the
examples/ directory.

API FUNCTIONS CURRENTLY IMPLEMENTED
-----------------------------------

Currently the library has implementations for the following API
functions:

* ListTopLevelEvents
* GetEventSubTreeNoSelections
* GetPrices
* PlaceOrdersNoReceipt
* GetAccountBalances
* ListBootstrapOrders
* ListOrdersChangedSince
* CancelOrders
* GetMarketInformation (currently outputs 'raw' data from Betdaq)
* ListBlacklistInformation (currently outputs 'raw' data from Betdaq)


TODO
----

Currently only a subset of the complete Betdaq API functionality is
implemented.  While this subset is sufficient to build a trading
application, some of the other methods do have their uses.  In
particular, additional methods for updating, cancelling, and
suspending orders would be handy.  There are quite a few of these
methods (all of which are 'secure' rather than 'readonly' in Betdaq
API jargon):

* UpdateOrdersNoReceipt
* CancelAllOrdersOnMarket
* CancelAllOrders
* SuspendFromTrading
* UnsuspendFromTrading
* SuspendOrders
* SuspendAllOrdersOnMarket
* SuspendAllOrders
* UnsuspendOrders

Other things to do
* Unit tests
* Better docs for the API functions
