"""Represents a portfolio."""

import datetime
import math

from analysis.trading import market_lib
from tool import logging
from tool import t


class PortfolioException(Exception):
  pass


class TransactionException(PortfolioException):
  pass


class Portfolio:
  def __init__(
      self,
      market: market_lib.Market,
      creation_datetime: datetime.datetime,
      initial_fund: float,
      initial_stocks: t.Dict[str, int] = None,
      limit_datetime: datetime.datetime = None):
    """Constructor.

    Args:
      market: the market used to loop up prices.
      creation_datetime: when the portfolio was created.
      initial_fund: the initial fund.
      initial_stocks: {symbol: amount}, stocks possessed initially.
      limit_datetime: no transaction can be made beyond this
          datetime. Making a transaction beyond this datetime causes an
          exception. Leaving as None means there is no limit.
    """
    if (limit_datetime and
            limit_datetime < creation_datetime):
      raise PortfolioException(
        'creation datetime (%s) cannot be greater then limit transaction '
        'datetime (%s)' % (creation_datetime, limit_datetime))

    if initial_fund < 0:
      raise PortfolioException(
        'initial fund (%s) must be positive' % initial_fund)

    self._market = market
    self._limit_datetime = limit_datetime

    # Represents the current datetime of the portforlio. Making a transaction
    # advances this datetime.
    self._current_datetime = creation_datetime
    # Remaining fund.
    self._fund = initial_fund
    # The actual portfolio: { symbol: number of possessed stocks }
    if initial_stocks:
      self._stocks = initial_stocks
    else:
      self._stocks = {}

  def Copy(self, initial_datetime: datetime.datetime = None):
    """Creates a copy of self.

    Args:
      initial_datetime: if leaving as None, the stored current_datetime is used.
    """
    if not initial_datetime:
      initial_datetime = self._current_datetime
    return Portfolio(
      self._market,
      initial_datetime,
      self._fund,
      initial_stocks=self._stocks.copy(),
      limit_datetime=self._limit_datetime)

  def GetMarket(self) -> market_lib.Market:
    return self._market

  def GetCurrentDatetime(self) -> datetime.datetime:
    return self._current_datetime

  def GetLimitDatetime(self) -> datetime.datetime:
    return self._limit_datetime

  def GetFund(self) -> float:
    return self._fund

  def GetShares(self) -> t.Dict[str, int]:
    return self._stocks.copy()

  def AdvanceDatetime(self, new_datetime: datetime.datetime):
    """Advances the stored datetime to the new value."""
    if new_datetime < self._current_datetime:
      raise TransactionException(
        'after a portfolio is created, its datetime can only be advances to a '
        'larger value; changing current datetime %s to %s is therefore '
        'forbidden.' % (
          new_datetime,
          self._current_datetime))
    self._current_datetime = new_datetime

  def MakeTransaction(
      self,
      symbol: str,
      amount: int,
      transaction_datetime: datetime.datetime = None):
    """Makes a transaction on the given datetime.

    Args:
      symbol: the symbol of the stock to trade.
      amount: the amount to trade. Positive means to buy, negative means to
          sell. If the buy/sell amount is beyond the capacity, the max
          capacity will be applied.
      transaction_datetime: when the transaction is made. This datetime can
          only be greater or equal than the last transaction datetime
          (can get using GetCurrentDatetime), and no larger then the limit
          transaction datetime (if set, can get using GetLimitDatetime).
          Leaving this as None means the transaction is made at the same time
          as last transaction. Making a transaction advances the internal
          state recording the last transaction datetime.

    Returns:
      Self, for chained actions.
    """
    if not transaction_datetime:
      transaction_datetime = self._current_datetime

    if transaction_datetime < self._current_datetime:
      raise TransactionException(
        'attempted transaction datetime (%s) is before the last transaction '
        'datetime (%s)' % (
          transaction_datetime,
          self._current_datetime))

    if (self._limit_datetime and
            transaction_datetime > self._limit_datetime):
      raise TransactionException(
        'attempted transaction datetime (%s) is beyond the limit transaction '
        'datetime (%s)' % (
          transaction_datetime,
          self._limit_datetime))

    self._stocks.setdefault(symbol, 0)
    price = self._market.GetPriceByDatetime(symbol, transaction_datetime)
    price = max(price, 1e-7)

    if amount > 0:
      # buy
      if price * amount > self._fund:
        buy_amount = math.floor(self._fund / price)
        logging.debug(
          'current fund (%s) is not enough to buy %s %s stocks; buy %d '
          'instead.',
          self._fund, amount, symbol, buy_amount)
      else:
        buy_amount = amount
      self._fund -= price * buy_amount
      self._stocks[symbol] += buy_amount
    else:
      # sell
      amount = -amount
      if amount > self._stocks[symbol]:
        logging.debug(
          'want to sell %s %s stocks; but holding only %d; sell all.',
          amount, symbol, self._stocks[symbol])
        sell_amount = self._stocks[symbol]
      else:
        sell_amount = abs(amount)
      self._fund += price * sell_amount
      self._stocks[symbol] -= sell_amount

    self.AdvanceDatetime(transaction_datetime)
    return self

  def BuyAll(
      self,
      symbol: str,
      transaction_datetime: datetime.datetime = None):
    """Uses all fund to buy a single stock."""
    return self.MakeTransaction(
      symbol, math.inf, transaction_datetime=transaction_datetime)

  def SellAll(
      self,
      symbol: str,
      transaction_datetime: datetime.datetime = None):
    """Sells all shares of the given stock."""
    return self.MakeTransaction(
      symbol, -math.inf, transaction_datetime=transaction_datetime)

  def Evaluate(
      self,
      evaluation_datetime: datetime.datetime = None) -> float:
    """Evaluates the total value of the portfolio at the given datetime."""
    portfolio_copy = self.Copy()
    for symbol in self.GetShares().keys():
      portfolio_copy.SellAll(symbol, transaction_datetime=evaluation_datetime)
    return portfolio_copy.GetFund()
