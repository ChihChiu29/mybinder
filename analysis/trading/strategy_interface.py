"""Interface for a trading strategy."""

import datetime

from analysis.trading import portfolio_lib


class TradingStrategy:
  """Represents a trading strategy."""

  def PerformTrading(
      self,
      portfolio: portfolio_lib.Portfolio,
      trading_datetime: datetime.datetime):
    """Performs (optional) transactions at the given date.

    During an evaluation, this function will be called for a sequence of
    datetimes in order.

    When making a transaction, by default the transaction is made at
    trading_datetime. However you can override it; but keep in mind that a given
    portfolio's transactions can only be made in temporal order, so make sure
    the datetime you specify when making a transaction is between the current
    trading_datetime and the next one (usually they differ by a day).

    Args:
      portfolio: the portfolio.
      trading_datetime: the datetime that an optional trading can be made.
    """
    raise NotImplementedError(
      'Need to implement your strategy in this function')
