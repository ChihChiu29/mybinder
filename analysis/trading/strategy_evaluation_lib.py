"""For evaluating a strategy."""

import datetime

import pandas as pd

from analysis.trading import market_lib
from analysis.trading import portfolio_lib
from analysis.trading import strategy_interface
from tool import datetime_util
from tool import t
from tool import ts

WEEKDAYS = tuple(range(5))
EVERYDAY = tuple(range(7))


class EvaluationReport:
  """Helps to generate reports for a portfolio history."""

  report_datetime_format = '%Y-%m-%d'

  def __init__(
      self,
      portfolio_history: t.List[portfolio_lib.Portfolio]):
    """Constructor.

    Args:
      portfolio_history: the history of a portfolio ordered so that the first
          element is the earliest portfolio.
    """
    if not portfolio_history:
      raise RuntimeError('Evaluation report requires an non-empty history.')
    self.portfolio_history = portfolio_history

  def GetDetailedReport(self) -> pd.DataFrame:
    """Lists funds and stock shares in history."""
    all_stock_symbols = set()
    for portfolio in self.portfolio_history:
      all_stock_symbols.update(portfolio.GetShares().keys())

    columns = [
                'timestamp',
                'datetime_str',
                'fund',
                'total_value'] + list(sorted(all_stock_symbols))
    history_df = pd.DataFrame(columns=columns)
    for portfolio in self.portfolio_history:
      row_dict = {
        'timestamp': portfolio.GetCurrentDatetime().timestamp(),
        'datetime_str': portfolio.GetCurrentDatetime().strftime(
          self.report_datetime_format),
        'fund': portfolio.GetFund(),
        'total_value': portfolio.Evaluate()}
      row_dict.update({
        symbol: portfolio.GetShares().get(symbol, 0)
        for symbol in all_stock_symbols})
      history_df = history_df.append(row_dict, ignore_index=True)
    return history_df

  def GetTotalValueTimeseries(self) -> ts.TimeSeries:
    """Returns the timeseries for the value of portfolio in history."""
    datetimes = self._GetDatetimes()
    values = [portfolio.Evaluate() for portfolio in self.portfolio_history]
    return ts.TimeSeries(datetimes, values)

  def GetStockShareTimeseries(self, symbol: str) -> ts.TimeSeries:
    """Returns the timeseries for the amount of stocks held in history."""
    datetimes = self._GetDatetimes()
    shares = [
      portfolio.GetShares().get(symbol, 0) for portfolio in
      self.portfolio_history]
    return ts.TimeSeries(datetimes, shares)

  def GetFinalDatetime(self) -> datetime.datetime:
    """Gets the last datetime in the history."""
    return self.portfolio_history[-1].GetCurrentDatetime()

  def GetFinalTotalValue(self) -> float:
    """Gets the final value of the portfolio."""
    return self.portfolio_history[-1].Evaluate()

  def _GetDatetimes(self) -> t.List[float]:
    """Returns the datetimes as a list in history."""
    return [
      portfolio.GetCurrentDatetime().timestamp() for portfolio in
      self.portfolio_history]


def EvaluateStrategy(
    market: market_lib.Market,
    strategy: strategy_interface.TradingStrategy,
    start_datetime: datetime.datetime,
    end_datetime: datetime.datetime,
    initial_fund: float,
    valid_weekdays: t.Iterable[int] = WEEKDAYS) -> EvaluationReport:
  """Evaluates a strategy.

  A portfolio will be created to simulate the strategy.

  Args:
    market: the market environment.
    strategy: the strategy to evaluate.
    start_datetime: the time initial fund was deposited.
    end_datetime: the final time performance is evaluated.
    initial_fund: the initial fund.
    valid_weekdays: the valid trading weekdays, refer to datetime.weekday
        function.

  Returns:
    The evaluation report. Use the report to get more info on the strategy.
  """
  portfolio = portfolio_lib.Portfolio(
    market,
    start_datetime,
    initial_fund,
    initial_stocks=None,
    limit_datetime=end_datetime)

  portfolio_history = []
  for day in datetime_util.DaysBetween(start_datetime, end_datetime):
    # Set the default trading time to the current day.
    portfolio.AdvanceDatetime(day)

    if day.weekday() not in valid_weekdays:
      continue
    strategy.PerformTrading(portfolio, day)
    portfolio_history.append(portfolio.Copy(initial_datetime=day))

  return EvaluationReport(portfolio_history)
