"""Generate memoryless daily-fluctuating timeseries.

Here "memoryless" means that the fluctuation on each day is independent of the
history.
"""
import datetime
import random
import typing

from tool import datetime_util
from tool import ts


def GenerateTimeSeriesWithFluctuation(
    start_datetime: datetime.datetime,
    end_datetime: datetime.datetime,
    initial_value: float,
    daily_delta_fn: typing.Callable[[], float],
) -> ts.TimeSeries:
  """Creates a timeseries using memoryless fluctuation.

  Args:
    start_datetime: the start datetime.
    end_datetime: the end datetime.
    initial_value: the initial value.
    daily_delta_fn: the function that returns a value specifying the change of
        the value in the timeseries relative to the value of the previous day.

  Returns:
    A timeseries with memoryless fluctuation.
  """
  current_value = None
  time_list = []
  value_list = []
  for day in datetime_util.DaysBetween(start_datetime, end_datetime):
    if current_value is None:
      current_value = initial_value
    else:
      current_value += daily_delta_fn()
      if current_value < 0:
        current_value = 0

    time_list.append(day.timestamp())
    value_list.append(current_value)
  return ts.TimeSeries(time_list, value_list)


class DeltaFunction:
  """Collection of delta functions to help generating timeseries."""

  @staticmethod
  def Uniform(a: float, b: float) -> typing.Callable[[], float]:
    def fn() -> float:
      return random.uniform(a, b)

    return fn
