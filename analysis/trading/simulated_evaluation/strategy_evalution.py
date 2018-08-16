"""Evaluates strategy using simulated markets."""
import datetime

from analysis.trading import strategy_evaluation_lib
from analysis.trading.simulated_evaluation import market_generation
from tool import t

DEFAULT_NUM_SIMULATIONS = 100

DEFAULT_START_DATETIME = datetime.datetime(2010, 1, 1)
DEFAULT_END_DATETIME = datetime.datetime(2011, 12, 31)


class SingleStockStrategyEvaluation:
  @staticmethod
  def EvaluateUsingFreeMarket(
      # strategy_interface.TradingStrategy subclass
      strategy_class: t.Callable[[], None],
      market_start_datetime: datetime.datetime = DEFAULT_START_DATETIME,
      market_end_datetime: datetime.datetime = DEFAULT_END_DATETIME,
      initial_stock_price: float = 1000,
      stock_daily_expected_change: float = 5,
      stock_daily_fluctuation: float = 200,
      initial_fund: float = 100000,
      num_simulations=DEFAULT_NUM_SIMULATIONS,
  ) -> t.List[float]:
    """Evaluate a strategy using a free market.

    Returns:
      A list of "actual return rate" divided by "expected return rate" for all
      simulations.
    """
    evaluation_results = []
    for _ in range(num_simulations):
      market = market_generation.CreateFreeFluctuatingMarket(
        start_datetime=market_start_datetime,
        end_datetime=market_end_datetime,
        num_symbols=1,
        init_value=initial_stock_price,
        fluctuation_center=stock_daily_expected_change,
        fluctuation_strength=stock_daily_fluctuation)

      initial_fund = float(initial_fund)
      report = strategy_evaluation_lib.EvaluateStrategy(
        market,
        strategy_class(),
        market_start_datetime,
        market_end_datetime,
        initial_fund)
      final_fund = report.GetFinalTotalValue()
      actual_return_rate = final_fund / initial_fund - 1
      expected_return_rate = market.GetStockMetadata(
        market.ListSymbols()[0]).expected_overall_return_rate

      evaluation_results.append(actual_return_rate / expected_return_rate)
    return evaluation_results
