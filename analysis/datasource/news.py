"""News reader for analysis."""

from absl import app

from datacollection.provider import article_provider
from datastruct import news
from tool import datetime_util
from tool import logging
from tool import t


class ArticleProvider:
  def __init__(self):
    self._article_manager = article_provider.GetArticleManager()

  def GetArticlesInMonth(
      self,
      year_month: datetime_util.YearMonth) -> t.List[news.Article]:
    """Return all articles in a given month."""
    return self._article_manager.GetArticlesBetween(
      year_month.FirstDay(), year_month.LastDay())

  def GetArticlesByMonth(
      self) -> (datetime_util.YearMonth, t.Iterable[t.List[news.Article]]):
    """Yield articles month by month."""
    start_year_month = datetime_util.YearMonthFromDatetime(
      self._article_manager.GetEarliestDatetime())
    end_year_month = datetime_util.YearMonthFromDatetime(
      self._article_manager.GetLatestDatetime())

    for year_month in datetime_util.MonthsBetween(
        start_year_month, end_year_month):
      yield (year_month, self.GetArticlesInMonth(year_month))


def main(_):
  provider = ArticleProvider()
  for year_month, articles in provider.GetArticlesByMonth():
    logging.info('%s: %d articles', year_month.YYYYMM(), len(articles))


if __name__ == '__main__':
  app.run(main)
