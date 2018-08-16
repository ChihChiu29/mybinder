"""Make using notebook during prototyping easier."""
import importlib

from analysis.sentiment import sentiment
from analysis.trading import market_generation
from analysis.trading import strategy_evaluation_lib
from analysis.trading.simulated_evaluation import \
  market_generation as simulated_market_generation
from analysis.trading.simulated_evaluation import strategy_evalution
from analysis.trading.strategy import single_stock_simple_strategies


class Collection:
  def __init__(self, **kwargs):
    for attr_name, attr_value in kwargs.items():
      self.__setattr__(attr_name, attr_value)


def CreateCollection():
  return Collection(
    analysis=Collection(
      sentiment=sentiment,
      trading=Collection(
        market_generation=market_generation,
        simulated=Collection(
          market_generation=simulated_market_generation,
          strategy_evaluation=strategy_evalution,
        ),
        strategy=Collection(
          single_stock_simple_strategies=single_stock_simple_strategies,
        ),
        strategy_evaluation_lib=strategy_evaluation_lib,
      )
    )
  )


def ReloadAllModulesInCollection(
    c: Collection,
    indent: int = 0,
) -> None:
  for attr_name, attr_value in vars(c).items():
    if isinstance(attr_value, Collection):
      print(' ' * indent + '[%s]' % attr_name)
      ReloadAllModulesInCollection(attr_value, indent=indent + 4)
    try:
      importlib.reload(attr_value)
      print(' ' * indent + '-- %s' % attr_name)
    except TypeError:
      pass
