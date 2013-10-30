# apiparse.py
# James Mithen
# jamesmithen@gmail.com

"""
Functions for parsing the data received from BDAQ Api calls.  The
SUDS library has done most of the work for us here, we just need to
extract the data we want.
"""

import const
import util
from exchange import *
from apiexception import ApiError

def ParseListTopLevelEvents(resp):
    events = []
    for ec in resp.EventClassifiers:
        events.append(Event(ec._Name, ec._Id, **dict(ec)))
    return events

def ParseGetEventSubTreeNoSelections(resp):
    # first thing is return status
    # return code below should be zero if successful
    retcode = resp.ReturnStatus._Code
    tstamp = resp.Timestamp    
    # check the Return Status is zero (success)
    # and not:
    # 5   - event classifier does not exist
    # 137 - maximuminputrecordsexceeded
    # 406 - punter blacklisted
    if retcode == 406:
        raise ApiError, 'punter is blacklisted'
    
    allmarkets = []
    markets = []
    # go through each event class in turn, an event class is
    # e.g. 'Rugby Union','Formula 1', etc.
    # slight trick here:
    # if we only polled a single event class, then resp[2] is
    # not a list, so we need to convert it to a list
    if isinstance(resp[2], list):
        data = resp[2]
    else:
        data = [resp[2]]
    for evclass in data:
        _ParseEventClassifier(evclass,'', markets)
        allmarkets = allmarkets + markets
    # hack: currently markets are duplicated multiple times (is this
    # an API error?); we want only unique markets here
    umarkets = util.unique(allmarkets)
    return umarkets

def _ParseEventClassifier(eclass, name='', markets=[]):
    """
    Get Markets from a Top Level Event, e.g. 'Rugby Union'.
    Note that we skip a level here, e.g. We would go Rugby ->
    Lions Tour -> market, but here we will just find all rugby
    union markets, regardless of their direct ancester.
    """

    name = name + '|' + eclass._Name
    pid = eclass._ParentId
    myid = eclass._Id

    if hasattr(eclass, 'EventClassifiers'):
        for e in eclass.EventClassifiers:
            _ParseEventClassifier(e, name, markets)
    else:
        if hasattr(eclass, 'Markets'):
            for mtype in eclass.Markets:
                markets.append(Market(name + '|' + mtype._Name,
                                      mtype._Id,
                                      pid,
                                      mtype._IsCurrentlyInRunning,
                                      **dict(mtype)))

def ParseGetPrices(marketids, resp):
    retcode = resp.ReturnStatus._Code
    tstamp = resp.Timestamp

    # check the Return Status is zero (success)
    # and not:
    # 8   - market does not exist
    # 16  - market neither suspended nor active
    # 137 - maximuminputrecordsexceeded (should never get this)
    # 406 - punter blacklisted
    if retcode == 406:
        raise ApiError, 'punter is blacklisted'

    # if we only called with a single market id, we won't have a list
    if len(marketids) == 1:
        resp.MarketPrices = [resp.MarketPrices]
        
    # check market prices is right length
    assert len(resp.MarketPrices) == len(marketids)

    allselections = []
    for (mid, mprice) in zip(marketids, resp.MarketPrices):
        # list of selections for this marketid
        allselections.append([])
        # go through each selection for the market.  For some reason
        # the Api is returning every selection twice, although this
        # could be an error with the SOAP library (?).

        # are there any selections?
        if not hasattr(mprice,'Selections'):
            # can reach here if market suspended
            break

        nsel = len(mprice.Selections)

        # we store the market withdrawal sequence number in every
        # selection instance, since this is needed to place a bet on
        # the selection.  This is mainly important for horse racing
        # markets, for which there are often withdrawals before the
        # race (i.e. horses that do not run), which in turn makes this
        # sequence number non-zero.  For other markets, the sequence
        # number is usually zero.
        wsn = mprice._WithdrawalSequenceNumber

        for sel in mprice.Selections[:nsel]:
            # lists of back and lay prices
            # note the response object may not have these attributes
            # if no odds are on offer
            if hasattr(sel, 'ForSidePrices'):
                # if we only have one price on offer
                # there is no array
                if (isinstance(sel.ForSidePrices,list)):
                    bprices = [(p._Price, p._Stake) for p in
                               sel.ForSidePrices]                    
                else:
                    bprices = [(sel.ForSidePrices._Price,
                                sel.ForSidePrices._Stake)]                    
            else:
                bprices = []
            if hasattr(sel, 'AgainstSidePrices'):
                # if we only have one price on offer
                # there is no array
                if (isinstance(sel.AgainstSidePrices,list)):
                    lprices = [(p._Price, p._Stake) for p in
                               sel.AgainstSidePrices]                    
                else:
                    # only one price
                    lprices = [(sel.AgainstSidePrices._Price,
                                sel.AgainstSidePrices._Stake)]
            else:
                lprices = []
            # create selection object using given data
            # we need to handle the case of no matches yet, since in
            # this case the response is missing certain fields.
            if not (sel._MatchedSelectionForStake or
                    sel._MatchedSelectionAgainstStake):
                lastmatchoccur = None
                lastmatchprice = None
                lastmatchamount = None
            else:
                lastmatchoccur = sel._LastMatchedOccurredAt
                lastmatchprice = sel._LastMatchedPrice
                lastmatchamount = sel._LastMatchedForSideAmount
            # the only data directly concerning the selection that we
            # are not storing in the selection instance is the
            # 'deduction factor'.
            allselections[-1].append(Selection(sel._Name, sel._Id, mid,
                                               sel._MatchedSelectionForStake,
                                               sel._MatchedSelectionAgainstStake,
                                               lastmatchoccur,
                                               lastmatchprice,
                                               lastmatchamount,
                                               bprices, lprices,
                                               sel._ResetCount, wsn,
                                               **dict(sel)))
    return allselections

def ParseListBootstrapOrders(resp):
    """
    Parse a single order, return order object.  Note there are a few
    things the Api is returning that we are ignoring here.
    """

    retcode = resp.ReturnStatus._Code
    tstamp = resp.Timestamp

    # check the return status here
    # some possible return codes are (see BDAQ docs for complete list):
    # 136 - WithdrawalSequenceNumberIsInvalid
    if retcode != 0:
        # will have to diagnose this in more detail if/when it happens.
        raise ApiError, ('Error with ListBootstrapOrders '
                         'return code {0}'.format(retcode))

    # no orders returned; end of bootstrapping process.
    if not hasattr(resp, 'Orders'):
        return {}

    # create and return list of order objects.    
    allorders = {}
    for o in resp.Orders.Order:
        sid = o._SelectionId
        ustake = o._UnmatchedStake
        mstake = o._MatchedStake
        stake = ustake + mstake
        # note we also get back '_MatchedPrice' if matched; this could
        # be better than '_RequestedPrice'.
        price = o._RequestedPrice
        pol = o._Polarity
        oref = o._Id
        status = o._Status
        
        allorders[oref] = Order(const.BDAQID, sid, stake, price,
                                pol, **{'oref': oref,
                                        'status': status,
                                        'matchedstake': mstake,
                                        'unmatchedstake': ustake})

    return allorders

def ParsePlaceOrdersNoReceipt(resp, olist):
    """Return list of order objects."""
    
    retcode = resp.ReturnStatus._Code
    tstamp = resp.Timestamp

    # check the return status here
    if retcode != 0:
        # will have to diagnose this in more detail if/when it happens.
        raise ApiError, ('Did not place order(s) succesfully, '
                         'return code {0}'.format(retcode))

    # list of order refs - I am presuming BDAQ returns them in the order
    # the orders were given!
    orefs = resp.OrderHandles.OrderHandle

    # create and return order object.  Note we set status to UNMATCHED,
    # and unmatched stake and matched stake accordingly.
    allorders = {}
    for (o, ref) in zip(olist, orefs):
        allorders[ref] = Order(o.sid, o.stake, o.price, o.polarity,
                               **{'oref': ref,
                                  'status': O_UNMATCHED,
                                  'matchedstake': 0.0,
                                  'unmatchedstake': o.stake})
    return allorders

def ParseCancelOrders(resp, olist):
    """Return list of order objects."""
    
    retcode = resp.ReturnStatus._Code
    tstamp = resp.Timestamp

    # check the return status here
    if retcode != 0:
        raise ApiError, ('Did not cancel order(s) succesfully, '
                         'return code {0}'.format(retcode))

    for o in resp.Orders.Order:
        oref = o._OrderHandle
        # find the order ref in the list of orders
        for myo in olist:
            if myo.oref == oref:
                myo.status = O_CANCELLED
                break
    return olist

def ParseGetAccountBalances(resp):
    """
    Returns account balance information by parsing output from BDAQ
    Api function GetAccountBalances.
    """
    retcode = resp.ReturnStatus._Code
    tstamp = resp.Timestamp

    # check the Return Status is zero (success)
    # and not:
    # 406 - punter blacklisted
    if retcode == 406:
        raise ApiError, 'punter is blacklisted'

    # Return tuple of _AvailableFunds, _Balance, _Credit, _Exposure
    return (resp._AvailableFunds, resp._Balance,
            resp._Credit, resp._Exposure)

def ParseListOrdersChangedSince(resp):
    """Returns list of orders that have changed"""
    retcode = resp.ReturnStatus._Code
    tstamp = resp.Timestamp

    # check the Return Status is zero (success)
    # and not:
    # 406 - punter blacklisted
    # 310 - sequence number less than zero
    if retcode == 406:
        raise ApiError, 'punter is blacklisted'
    elif retcode == 310:
        raise ApiError, 'sequence number cannot be less than zero'

    if not hasattr(resp, 'Orders'):
        # no orders have changed
        return {}

    # store the sequence numbers of the orders: we need to return the
    # maximum sequence number so that the next time we call the Api
    # function we won't return this again!
    seqnums = []

    allorders = {}
    for o in resp.Orders.Order:

        # From API docs, order _Status can be
        # 1 - Unmatched.  Order has SOME amount available for matching.
        # 2 - Matched (but not settled).
        # 3 - Cancelled (at least some part of the order was unmatched).
        # 4 - Settled.
        # 5 - Void.
        # 6 - Suspended.  At least some part unmatched but is suspended.

        # Note: at the moment we are not storing all of the data that
        # comes from the BDAQ API function, only the information that
        # seems useful...
        odict = {'oref': o._Id,
                 'status': o._Status,
                 'matchedstake' : o._MatchedStake,
                 'unmatchedstake': o._UnmatchedStake}

        allorders[o._Id] = Order(const.BDAQID, o._SelectionId,
                                 o._MatchedStake + o._UnmatchedStake,
                                 o._RequestedPrice, o._Polarity,
                                 **odict)
        # store sequence number
        seqnums.append(o._SequenceNumber)

    return allorders, max(seqnums)
