"""Stock price reader for analysis."""
from absl import app

from datacollection.provider import stock_provider
from tool import datetime_util
from tool import t
from tool import ts

_DEFAULT_SYMBOL = 'GOOG'


class PriceProvider:
  def __init__(self):
    self.price_timeseries = stock_provider.GetStockTimeSeriesFromDir()

  def GetStockSymbols(self) -> t.Set[str]:
    return set(self.price_timeseries.keys())

  def GetDailyPriceTimeseries(
      self,
      symbol: str = _DEFAULT_SYMBOL) -> ts.TimeSeries:
    """Return daily interpolated prices."""
    time_series = []
    price_series = []
    for day in datetime_util.DaysBetween(
        self.price_timeseries[symbol].GetMinDatetime(),
        self.price_timeseries[symbol].GetMaxDatetime()):
      time_series.append(day.timestamp())
      price_series.append(
        self.price_timeseries[symbol].GetValueByTimestamp(day.timestamp()))

    return ts.TimeSeries(time_series, price_series)

  def GetMonthlyPriceTimeseries(
      self,
      symbol: str = _DEFAULT_SYMBOL) -> ts.TimeSeries:
    """Return monthly averaged prices."""
    start_year_month = datetime_util.NextMonth(
      datetime_util.YearMonthFromDatetime(
        self.price_timeseries[symbol].GetMinDatetime()))
    end_year_month = datetime_util.PreviousMonth(
      datetime_util.YearMonthFromDatetime(
        self.price_timeseries[symbol].GetMaxDatetime()))

    time_series = []
    price_series = []
    for ym in datetime_util.MonthsBetween(start_year_month, end_year_month):
      time_series.append(ym.FirstDay().timestamp())
      price_series.append(self.price_timeseries[symbol].GetAverage(
        ym.FirstDay().timestamp(), ym.LastDay().timestamp()))

    return ts.TimeSeries(time_series, price_series)

  def GetMonthlyPriceDifferenceTimeseries(
      self,
      symbol: str = _DEFAULT_SYMBOL,
      diff_by_num_of_months: int = 1) -> t.Tuple[ts.TimeSeries, ts.TimeSeries]:
    """Return timeseries for difference of monthly averaged price timeseries.

    Args:
      symbol: the symbol of a stock.
      diff_by_num_of_months: see explanation in returns section.

    Returns:
      (price-difference timeseries, price-difference-percentage timeseries)

      If m=diff_by_num_of_months and the monthly average price is A(i) for a
      given month, i=1..n, then the returned price-difference timeseries is:
        A(i+m)-A(i), for i=1..n-m
      The price-difference-percentage timeseries is:
        (A(i+m)-A(i)) / A(i), for i=1..n-m
    """
    monthly_avg = self.GetMonthlyPriceTimeseries(symbol=symbol)
    time_array = monthly_avg.GetTimeArray()
    value_array = monthly_avg.GetValueArray()

    n = time_array.size
    m = diff_by_num_of_months
    diff_time_array = time_array[:n - m]
    diff_value_array = value_array[m:] - value_array[:n - m]
    diff_value_percentage_array = 100.0 * diff_value_array / value_array[:n - m]

    return (
      ts.TimeSeries(diff_time_array, diff_value_array),
      ts.TimeSeries(diff_time_array, diff_value_percentage_array))


def main(_):
  provider = PriceProvider()
  provider.GetDailyPriceTimeseries().Plot()
  provider.GetMonthlyPriceTimeseries().Plot()
  diff_ts = provider.GetMonthlyPriceDifferenceTimeseries()
  diff_ts[0].Plot()
  diff_ts[1].Plot()
  diff_ts = provider.GetMonthlyPriceDifferenceTimeseries(
    diff_by_num_of_months=3)
  diff_ts[0].Plot()
  diff_ts[1].Plot()


if __name__ == '__main__':
  app.run(main)
