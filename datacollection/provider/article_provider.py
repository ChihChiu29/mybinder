"""Provide articles."""
import datetime

from absl import app

from datacollection.processor import nytimes
from datastruct import news
from tool import file
from  tool import t


class ArticleManager:
  def __init__(
      self,
      json_pickle_file_path: str = '',
      pickle_file_path: str = ''):
    """Constructor.

    Args:
      json_pickle_file_path: the path to the json pickle file saved by
          nytimes.ArticleMixer.
      pickle_file_path: the path to the pickle file saved by
          nytimes.ArticleMixer.
    """
    provider = nytimes.ArticleMixer()
    if json_pickle_file_path:
      provider.FromJsonPickle(file.ReadData(json_pickle_file_path))
    elif pickle_file_path:
      provider.FromPickle(file.ReadByteData(pickle_file_path))
    else:
      raise RuntimeError('Need to specify at least one file path.')
    self._articles = provider.GetArticles()
    if not self._articles:
      raise RuntimeError('No article found.')

  def GetArticlesBetween(
      self,
      start_datetime: datetime.datetime,
      end_datetime: datetime.datetime) -> t.List[news.Article]:
    """Returns a list of articles (copy) in the given range."""
    if start_datetime > end_datetime:
      return []

    start_index = 0
    for article in self._articles:
      if start_datetime > article.pub_time:
        start_index += 1
      else:
        break

    end_index = len(self._articles)
    for article in reversed(self._articles):
      if end_datetime < article.pub_time:
        end_index -= 1
      else:
        break

    return self._articles[start_index:end_index]

  def GetEarliestDatetime(self) -> datetime.datetime:
    return self._articles[0].pub_time

  def GetLatestDatetime(self) -> datetime.datetime:
    return self._articles[-1].pub_time


def GetArticleManager():
  return ArticleManager(pickle_file_path='google_nytimes_articles.pickle')


def main(_):
  # article_manager = ArticleManager(
  #   json_pickle_file_path='google_nytimes_articles.json')
  article_manager = ArticleManager(
    pickle_file_path='google_nytimes_articles.pickle')
  print(article_manager)


if __name__ == '__main__':
  app.run(main)
