"""Provides simulated markets."""
import datetime

from analysis.trading.simulated_evaluation import controlled_market_lib
from analysis.trading.simulated_evaluation import free_fluctuating_timeseries

DEFAULT_START_DATETIME = datetime.datetime(year=2000, month=1, day=1)
DEFAULT_END_DATETIME = datetime.datetime(year=2015, month=12, day=31)

DEFAULT_NUM_STOCKS = 10


def CreateFreeFluctuatingMarket(
    start_datetime: datetime.datetime = DEFAULT_START_DATETIME,
    end_datetime: datetime.datetime = DEFAULT_END_DATETIME,
    num_symbols: int = DEFAULT_NUM_STOCKS,
    init_value: float = 1000,
    fluctuation_center: float = 5,
    fluctuation_strength: float = 200,
) -> controlled_market_lib.ControlledMarket:
  """Creates a market with free fluctuating stocks.

  Args:
    start_datetime: market start datetime.
    end_datetime: market end datetime.
    num_symbols: how many symbols in the market.
    init_value: stock initial price.
    fluctuation_center: expectation value of the fluctuation.
    fluctuation_strength: the strength (magnitude) of the fluctuation.
  """
  market = controlled_market_lib.ControlledMarket()
  for idx in range(num_symbols):
    symbol = _CreateSymbol(idx)
    market.AddOrUpdateStockTimeSeries(
      symbol,
      free_fluctuating_timeseries.GenerateTimeSeriesWithFluctuation(
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        initial_value=init_value,
        daily_delta_fn=free_fluctuating_timeseries.DeltaFunction.Uniform(
          fluctuation_center - fluctuation_strength,
          fluctuation_center + fluctuation_strength)))
    market.AddOrUpdateStockMetadata(
      symbol,
      controlled_market_lib.StockMetadata(
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        initial_price=init_value,
        expected_daily_change=fluctuation_center))
  return market


def _CreateSymbol(idx: int) -> str:
  """Creates a symbol for the given index."""
  return 'STOCK_%d' % idx
