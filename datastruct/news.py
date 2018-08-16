"""News data structures."""

import datetime

from tool import t


class Keyword:
  def __init__(self):
    self.name = ''  # type: str
    self.value = ''  # type: str
    # Smaller rank means more important.
    self.rank = -1  # type: int


class Subject:
  def __init__(self):
    self.value = ''  # type: str
    # Smaller rank means more important.
    self.rank = -1  # type: int


class Summary:
  def __init__(self):
    self.snippet = ''  # type: str
    self.abstract = ''  # type: str
    self.headlines = []  # type: t.List[str]
    self.keywords = []  # type: t.List[Keyword]
    self.subjects = []  # type: t.List[Subject]


class Article:
  def __init__(self):
    self.url = ''  # type: str
    self.pub_time = (
      datetime.datetime.fromtimestamp(0))  # type: datetime.datetime
    self.summary = Summary()  # type: Summary
    self.stories = []  # type: t.List[str]
