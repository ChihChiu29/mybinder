"""Helps to limit the rate an action can happen."""
import time


class SingleThreadThrottler(object):
  def __init__(self, limit_rate: float):
    """Constructor.

    Args:
      limit_rate (float): desired number of actions per second.
    """
    self._last_action_time_sec = time.time()
    self._delta_time_sec = 1.0 / limit_rate

  def WaitUntilNextAllowedTime(self):
    to_sleep_sec = self._delta_time_sec - (time.time() -
                                           self._last_action_time_sec)
    time.sleep(to_sleep_sec if to_sleep_sec > 0 else 0)
    self._last_action_time_sec = time.time()
