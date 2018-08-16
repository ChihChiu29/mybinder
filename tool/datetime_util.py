"""Helps manage dates."""

import datetime

from dateutil import relativedelta
from dateutil import rrule

from tool import t


class YearMonth:
  def __init__(self, year: int, month: int):
    self.year = year
    self.month = month

  def FirstDay(self) -> datetime.datetime:
    return datetime.datetime(self.year, self.month, 1)

  def LastDay(self) -> datetime.datetime:
    # See: https://stackoverflow.com/a/14994380
    return self.FirstDay() + relativedelta.relativedelta(day=31)

  def YYYYMM(self) -> str:
    return '%04d%02d' % (self.year, self.month)


def YearMonthFromDatetime(dt: datetime) -> YearMonth:
  return YearMonth(dt.year, dt.month)


def NextMonth(year_month: YearMonth) -> YearMonth:
  return YearMonthFromDatetime(
    year_month.FirstDay() + relativedelta.relativedelta(days=31))


def PreviousMonth(year_month: YearMonth) -> YearMonth:
  return YearMonthFromDatetime(
    year_month.FirstDay() - relativedelta.relativedelta(days=31))


def CurrentMonth() -> YearMonth:
  return YearMonthFromDatetime(datetime.datetime.today())


def MonthsBetween(
    start: YearMonth,
    end: YearMonth = None) -> t.Iterable[YearMonth]:
  """List months between two YearMonths, including "end"."""
  for dt in rrule.rrule(
      rrule.MONTHLY,
      dtstart=start.FirstDay(),
      until=end.FirstDay()):
    yield YearMonthFromDatetime(dt)


def NextDay(day: datetime.datetime) -> datetime.datetime:
  return day + relativedelta.relativedelta(days=1)


def PreviousDay(day: datetime.datetime) -> datetime.datetime:
  return day - relativedelta.relativedelta(days=1)


def DaysBetween(
    start: datetime.datetime,
    end: datetime.datetime) -> t.Iterable[datetime.datetime]:
  """List days between two datetimes, including "end"."""
  return rrule.rrule(rrule.DAILY, dtstart=start.date(), until=end.date())
