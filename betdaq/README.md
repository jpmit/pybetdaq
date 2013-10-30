PyBetdaq
========

PyBetdaq is an interface to the Betdaq sports exchange
(www.betdaq.com) API written in Python.  This allows trading
applications that place orders on the Betdaq exchange to be built in
Python.

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
betdaq/ directory.  Add the path to this directory to your PYTHONPATH
environment variable.

To use the library in a Python program, write
```python
import betdaq
```

The Betdaq API functions are then available in the betdaq namespace.
For example,
```python
betdaq.ListTopLevelEvents()
```
will return a list of Event objects, each representing a top level
event e.g. 'Horse Racing' or 'Soccer'.

As well as 'Event' objects in the example above, the library defines
'Market', 'Selection' and 'Order' objects, which are designed to be
useful abstractions for trading applications.  The library functions
typically return lists of these objects.  For example,
```python
betdaq.GetEventSubTreeNoSelections([100004])
```
will return a list of Market objects for the top level event with id
100004 (which happens to be Horse Racing).  And
```python
betdaq.GetPrices([111, 112])
```

where 111 and 112 are market ids (which do not correspond to real
market ids in this example) will return a list of length 2 -
[[sel111_1, sel111_2, ...], [sel112_1, sel112_2, ...]] - where each
list item is a list of selection objects (the first item is a list of
selection objects for the market with id 111, the second item the same
for market id 112).

Further examples of how to use the library functions together to
produce a simple trading application are given in the examples/
directory.

API FUNCTIONS IMPLEMENTED
-------------------------

Currently the library has implementations for the following API functions:
* ListTopLevelEvents
* GetEventSubTreeNoSelections
* GetPrices
* GetMarketInformation
* PlaceOrdersNoReceipt
* GetAccountBalances
* ListBootstrapOrders
* ListOrdersChangedSince
* ListBlackListInformation

TODO
----

Currently only a subset of the complete Betdaq API functionality is
implemented.  While this subset is sufficient to build a trading
application, some of the other methods do have their uses.  In
particular, methods for updating, cancelling, and suspending orders
would be handy.  There are quite a few of these methods (all of which
are 'secure' rather than 'readonly' in Betdaq API jargon):

* UpdateOrdersNoReceipt
* CancelAllOrdersOnMarket
* CancelAllOrders
* SuspendFromTrading
* UnsuspendFromTrading
* SuspendOrders
* SuspendAllOrdersOnMarket
* SuspendAllOrders
* UnsuspendOrders
