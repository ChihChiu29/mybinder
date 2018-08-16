"""This strategy does not perform any price-based buy/sell actions."""
import datetime
import random

from dateutil import relativedelta

from analysis.trading import portfolio_lib
from analysis.trading import strategy_interface


class AbstractSingleStockStrategy(strategy_interface.TradingStrategy):
  def __init__(self, use_symbol=None):
    self._use_symbol = use_symbol

  def GetSymbol(self, portfolio: portfolio_lib.Portfolio):
    if self._use_symbol:
      return self._use_symbol
    else:
      return portfolio.GetMarket().ListSymbols()[0]


class BuyThenHoldStrategy(AbstractSingleStockStrategy):
  """Use all fund to always buy the first stock."""

  def PerformTrading(
      self,
      portfolio: portfolio_lib.Portfolio,
      trading_datetime: datetime.datetime):
    portfolio.BuyAll(self.GetSymbol(portfolio))


class RandomStrategy(AbstractSingleStockStrategy):
  """Randomly buy or sell stocks."""

  def PerformTrading(
      self,
      portfolio: portfolio_lib.Portfolio,
      trading_datetime: datetime.datetime):
    portfolio.MakeTransaction(self.GetSymbol(portfolio), random.randint(-2, 3))


class PriceDerivativeTraderStrategy(AbstractSingleStockStrategy):
  """Uses stock price derivative to trade."""

  def PerformTrading(
      self,
      portfolio: portfolio_lib.Portfolio,
      trading_datetime: datetime.datetime):

    symbol = self.GetSymbol(portfolio)
    now = portfolio.GetMarket().GetPriceByDatetime(symbol, trading_datetime)
    hours_ago_1 = portfolio.GetMarket().GetPriceByDatetime(
      symbol, trading_datetime - relativedelta.relativedelta(hours=1))
    hours_ago_2 = portfolio.GetMarket().GetPriceByDatetime(
      symbol, trading_datetime - relativedelta.relativedelta(hours=2))
    days_ago_1 = portfolio.GetMarket().GetPriceByDatetime(
      symbol, trading_datetime - relativedelta.relativedelta(days=1))
    days_ago_2 = portfolio.GetMarket().GetPriceByDatetime(
      symbol, trading_datetime - relativedelta.relativedelta(days=2))

    if hours_ago_1 - hours_ago_2 > 0:
      portfolio.BuyAll(symbol)
    else:
      portfolio.SellAll(symbol)
