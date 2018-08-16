"""Provide articles."""
import os

from absl import app

from datacollection.processor import alpha_vantage
from tool import file
from tool import t
from tool import ts

_STOCKS_DIR = 'stocks'


def GetPriceTimeSeries() -> ts.TimeSeries:
  """Return a timeseries for price from saved pickle file."""
  reader = alpha_vantage.PriceJsonReader()
  reader.FromPickle(file.ReadByteData('google_alphavantage.pickle'))
  # reader.FromPickle(file.ReadByteData('apple_alphavantage.pickle'))
  return reader.GetPriceTimeSeries()


def GetStockTimeSeriesFromDir(
    stock_dir: str = _STOCKS_DIR) -> t.Dict[str, ts.TimeSeries]:
  """Returns a {symbol: price timeseries} dict from data files in a dir."""
  stocks = {}
  for filename in os.listdir(file.GetDataDirPath(stock_dir)):
    symbol = os.path.splitext(filename)[0]
    reader = alpha_vantage.PriceJsonReader()
    reader.FromPickle(file.ReadByteData(os.path.join(stock_dir, filename)))
    stocks[symbol] = reader.GetPriceTimeSeries()
  return stocks


def main(_):
  series = GetPriceTimeSeries()
  series.Plot()


if __name__ == '__main__':
  app.run(main)
