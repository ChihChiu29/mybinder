"""Represent a market environment."""
import datetime

from tool import t
from tool import ts


class MarketInfoQueryException(Exception):
  pass


class Market:
  def __init__(self):
    """Constructor.

    Use AddOrUpdateStockTimeSeries to add stock timeseries.
    """
    self._stocks = {}  # type: t.Dict[str, ts.TimeSeries]

  def CheckSymbol(self, symbol: str):
    if symbol not in self._stocks.keys():
      raise MarketInfoQueryException('no info found for "%s"' % symbol)

  def AddOrUpdateStockTimeSeries(
      self,
      symbol: str,
      timeseries: ts.TimeSeries):
    self._stocks[symbol] = timeseries

  def GetPriceByDatetime(
      self,
      symbol: str,
      dt: datetime.datetime) -> float:
    return self.GetPriceByTimestamp(symbol, dt.timestamp())

  def GetPriceByTimestamp(
      self,
      symbol: str,
      timestamp: float) -> float:
    """Get price of a stock at a given timestamp."""
    self.CheckSymbol(symbol)

    prices = self._stocks[symbol]
    min_timestamp = prices.GetMinTimestamp()
    max_timestamp = prices.GetMaxTimestamp()
    if timestamp < min_timestamp or timestamp > max_timestamp:
      raise MarketInfoQueryException(
        'timestamp %s is not in the allowed range',
        timestamp, min_timestamp, max_timestamp)

    return self._stocks[symbol].GetValueByTimestamp(timestamp)

  def GetPriceTimeSeries(
      self,
      symbol: str) -> ts.TimeSeries:
    self.CheckSymbol(symbol)
    return self._stocks[symbol]

  def ListSymbols(self) -> t.List[str]:
    return list(self._stocks.keys())

  def PlotAllSymbols(self) -> None:
    for symbol in self.ListSymbols():
      print('%s' % symbol)
      self.GetPriceTimeSeries(symbol).Plot()
