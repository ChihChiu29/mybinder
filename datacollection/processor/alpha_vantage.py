"""Process data fetched from Vantage."""
import json
import pickle

from absl import app
from dateutil import parser

from datastruct import stock
from tool import file
from tool import t
from tool import ts


class PriceJsonReader:
  """Provide stock.Price objects."""

  def __init__(self):
    self._price_series = []  # type: t.List[stock.InstantPrice]

  def GetPriceSeries(self) -> t.List[stock.InstantPrice]:
    """Return ordered prices."""
    return list(sorted(self._price_series, key=lambda p: p.time))

  def GetPriceTimeSeries(self) -> ts.TimeSeries:
    """Return prices as a timeseries."""
    price_series = self.GetPriceSeries()
    time_series = [price.time.timestamp() for price in price_series]
    price_series = [price.value for price in price_series]
    return ts.TimeSeries(time_series, price_series)

  def ReadJson(
      self,
      stock_json: t.JSON,
      use_price: str = '3. low'):
    """Reads a Alpha Vantage JSON.

    Args:
      stock_json: JSON data created by finance.alpha_vantage.
      use_price: which price to use. See JSON file to see the options.
    """
    for day, prices in stock_json['Time Series (Daily)'].items():
      price = stock.InstantPrice()
      price.time = parser.parse(day)
      price.value = float(prices[use_price])
      self._price_series.append(price)

  def ReadJsonFile(
      self,
      file_path: str,
      use_price: str = '3. low'):
    """Reads a Alpha Vantage JSON file saved by finance.alpha_vantage module.

    Args:
      file_path: JSON data file path relative to data directory.
      use_price: which price to use. See JSON file to see the options.
    """
    data = json.loads(file.ReadData(file_path))
    self.ReadJson(data, use_price=use_price)

  def ToPickle(self) -> bytes:
    return pickle.dumps(self._price_series)

  def FromPickle(self, pickle_bytes: bytes):
    self._price_series = pickle.loads(pickle_bytes)


def main(_):
  reader = PriceJsonReader()
  # reader.ReadJsonFile('google_alphavantage.json')
  # file.WriteByteData('google_alphavantage.pickle', reader.ToPickle())
  reader.ReadJsonFile('apple_alphavantage.json')
  file.WriteByteData('apple_alphavantage.pickle', reader.ToPickle())


if __name__ == '__main__':
  app.run(main)
