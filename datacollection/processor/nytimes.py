"""Process data fetched from NY Times."""

import json
import os
import pickle
import re
import typing

import jsonpickle
from absl import app
from absl import flags
from dateutil import parser

from datastruct import news
from tool import file
from tool import t

FLAGS = flags.FLAGS

flags.DEFINE_bool(
  'prototype', False,
  'whether to run in prototype mode')

# This keyword means the value is a subject.
_SUBJECT_KEYWORD = 'subject'


class ArticleMixer(object):
  """Mix summaries and stories into news.Article objects."""

  def __init__(self):
    self._articles = {}  # type: typing.Dict[str, news.Article]

  def GetArticles(self) -> t.List[news.Article]:
    """Return all articles as a list ordered by pub_time."""
    return list(sorted(self._articles.values(), key=lambda a: a.pub_time))

  def _GetArticle(self, url: str) -> news.Article:
    """Get the article with the given url, or create an empty one."""
    return self._articles.setdefault(url, news.Article())

  def ReadAllFiles(
      self,
      dir_path: str,
      summary_filename_regexp: str,
      story_filename_regexp: str) -> None:
    """Update states from all files in a directory.

    Args:
      dir_path: where to read files from, relative to data folder.
      summary_filename_regexp: if a filename matches this regexp, it is a
          summary file.
      story_filename_regexp: if a filename matches this regexp, it is a story
          file.
    """
    dir_path_full = file.GetDataDirPath(sub_dir=dir_path)
    for filename in os.listdir(dir_path_full):
      relative_path = os.path.join(dir_path, filename)
      if re.match(summary_filename_regexp, filename):
        self.ReadSummaryFile(relative_path)
      elif re.match(story_filename_regexp, filename):
        self.ReadStoryFile(relative_path)

  def ReadSummaryFile(self, filepath: str) -> None:
    """Update states from a summary json file.

    Args:
      filepath: path to the summary data file relative to the data folder.
    """
    summaries = json.loads(file.ReadData(filepath))
    for summary_json in summaries.values():
      article = self._GetArticle(summary_json['web_url'])
      article.url = summary_json['web_url']
      article.pub_time = parser.parse(summary_json['pub_date']).replace(
        tzinfo=None)
      summary = article.summary
      summary.snippet = summary_json.get('snippet', '')
      summary.abstract = summary_json.get('abstract', '')
      head_line = summary_json['headline']['main']
      if head_line:
        summary.headlines.append(head_line)
      head_line = summary_json['headline']['kicker']
      if head_line:
        summary.headlines.append(head_line)
      for keyword_json in summary_json['keywords']:
        if keyword_json['name'] == _SUBJECT_KEYWORD:
          subject = news.Subject()
          subject.value = keyword_json['value']
          subject.rank = keyword_json['rank']
          summary.subjects.append(subject)
        else:
          keyword = news.Keyword()
          keyword.name = keyword_json['name']
          keyword.value = keyword_json['value']
          keyword.rank = keyword_json['rank']
          summary.keywords.append(keyword)

  def ReadStoryFile(self, filepath: str) -> None:
    """Update states from a story json file.

    Args:
      filepath: path to the story data file relative to the data folder.
    """
    stories = json.loads(file.ReadData(filepath))
    for url, stories in stories.items():
      article = self._GetArticle(url)
      article.stories.extend(stories)

  def ToJsonPickle(self) -> str:
    return jsonpickle.encode(self._articles)

  def FromJsonPickle(self, json_str: str) -> None:
    self._articles = jsonpickle.decode(json_str)

  def ToPickle(self) -> bytes:
    return pickle.dumps(self._articles)

  def FromPickle(self, pickle_bytes: bytes):
    self._articles = pickle.loads(pickle_bytes)


def MixAll(
    summary_regexp: str = r'google_nytimes_\w*.json',
    story_regexp: str = r'stories_google_nytimes_\w*.json') -> ArticleMixer:
  mixer = ArticleMixer()
  for dir_path in ['nytimes_2014', 'nytimes_2015', 'nytimes_2016',
                   'nytimes_2017']:
    mixer.ReadAllFiles(dir_path, summary_regexp, story_regexp)
  return mixer


def Playground() -> ArticleMixer:
  mixer = ArticleMixer()
  mixer.ReadSummaryFile('nytimes_2014/google_nytimes_201401.json')
  mixer.ReadStoryFile('nytimes_2014/stories_google_nytimes_201401.json')
  return mixer


def main(_):
  if FLAGS.playground:
    mixer = Playground()
  else:
    mixer = MixAll()
  file.WriteData('google_nytimes_articles.jsonpickle', mixer.ToJsonPickle())
  file.WriteByteData('google_nytimes_articles.pickle', mixer.ToPickle())


if __name__ == '__main__':
  app.run(main)
