"""Real date market generation related function."""

from analysis.datasource import stock
from analysis.trading import market_lib


def CreateMarketFromData() -> market_lib.Market:
  data_provider = stock.PriceProvider()
  market = market_lib.Market()
  for symbol in data_provider.GetStockSymbols():
    market.AddOrUpdateStockTimeSeries(
      symbol, data_provider.GetDailyPriceTimeseries(symbol))
  return market
