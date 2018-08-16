"""Related to simulated markets where we have control on what to expect.

For example control can mean that we know expected annual gain rate etc.
"""
import datetime
import math

from analysis.trading import market_lib
from tool import datetime_util

_NUM_DAYS_PER_YEAR = 365.25  # 0.25 coming from leap year.
_NUM_MONTH_PER_YEAR = 12.0


class ControlledMarketError(Exception):
  pass


class StockMetadata:
  """Holds metadata for stocks."""

  def __init__(
      self,
      start_datetime: datetime.datetime,
      end_datetime: datetime.datetime,
      initial_price: float,
      expected_daily_change: float = None,
      expected_final_price: float = None):
    """Constructor.

    Args:
      start_datetime: when the stock date starts.
      end_datetime: when the stock data ends.
      initial_price: the initial price of the stock.
      expected_daily_change: expected daily change. If set, will ignore
          expected_final_price.
      expected_final_price: the expected final price of the stock. Note that
          this is not the actual final price of the stock, which is
          susceptible to fluctuation.
    """
    self.start_datetime = start_datetime
    self.end_datetime = end_datetime
    self.initial_price = float(initial_price)

    if not expected_daily_change and not expected_final_price:
      raise ControlledMarketError(
        'one of expected_daily_change or expected_final_price must be set')
    self.expected_daily_change = expected_daily_change
    self.expected_final_price = expected_final_price

    self.num_days = None
    self.num_months = None
    self.num_years = None
    self.expected_daily_return_rate = None
    self.expected_monthly_return_rate = None
    self.expected_annual_return_rate = None
    self.expected_overall_return_rate = None

    self._CalculateAttributes()

  def _CalculateAttributes(self):
    """Calculate induced attributes."""
    self.num_days = float(len(list(
      datetime_util.DaysBetween(self.start_datetime, self.end_datetime))))
    self.num_years = self.num_days / _NUM_DAYS_PER_YEAR
    self.num_months = self.num_years * _NUM_MONTH_PER_YEAR

    if self.expected_daily_change:
      self.expected_final_price = (
        self.initial_price + self.num_days * self.expected_daily_change)
    else:
      self.expected_daily_change = (
        (self.expected_final_price - self.initial_price) / self.num_days)

    self.expected_overall_return_rate = (
      (self.expected_final_price / self.initial_price) - 1)

    # (1 + annual_return_rate) ^ (num_years) = 1 + overall_return_rate
    self.expected_annual_return_rate = (
      math.pow(1 + self.expected_overall_return_rate, 1 / self.num_years) - 1)
    self.expected_monthly_return_rate = (
      math.pow(1 + self.expected_overall_return_rate, 1 / self.num_months) - 1)
    self.expected_daily_return_rate = (
      math.pow(1 + self.expected_overall_return_rate, 1 / self.num_days) - 1)


class ControlledMarket(market_lib.Market):
  """A controlled market has metadata for stocks."""

  def __init__(self):
    super().__init__()
    self._stock_metadata = {}

  def AddOrUpdateStockMetadata(
      self,
      symbol: str,
      metadata: StockMetadata,
  ) -> None:
    self._stock_metadata[symbol] = metadata

  def GetStockMetadata(
      self,
      symbol: str,
  ) -> StockMetadata:
    return self._stock_metadata.get(symbol, None)
