import json
from urllib import request

from joblib import Memory

from tool import file
from tool import logging
from tool import t

DISK_CACHE = Memory(
  cachedir=file.GetCacheDirPath('tool/nbshttp'),
  verbose=0)


@DISK_CACHE.cache
def JsonGET(url: str) -> t.JSON:
  """Gets a JSON over http GET.

  Args:
    url (string): the string to GET from.

  Returns:
    dict: the response JSON.
  """
  logging.info('Fetching from URL: %s', url)
  req = request.urlopen(url)

  return json.loads(req.read())
