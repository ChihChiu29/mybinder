"""Stock data structure."""

import datetime


class InstantPrice:
  def __init__(self):
    self.time = datetime.datetime.fromtimestamp(0)  # type: datetime.datetime
    self.value = 0  # type: float
