"""Read/write data files.

We have preferred directories for data files for reading/writing. This module
is to help enforce the read/write best practice. Whenever you read/write a data
file, use this module. For directory convention see tools.settings module.
"""

import os

_PROTOTYPE = True


def GetProjectRootPath() -> str:
  return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def GetDataDirPath(sub_dir: str = '') -> str:
  if _PROTOTYPE:
    return os.path.join(GetProjectRootPath(), 'data', 'prototype', sub_dir)
  else:
    return os.path.join(GetProjectRootPath(), 'data', sub_dir)


def GetCacheDirPath(cache_type_id: str) -> str:
  return os.path.join(GetProjectRootPath(), 'cache', cache_type_id)


def GetTmpDirPath(sub_dir: str = '') -> str:
  """Returns a tmp directory to dump data.

  Note that this directory is intended to be used as a temporary writing space,
  but the data files dumped to it will be kept/copied out. If you really need
  a "read" tmp folder, use tempfile module.
  """
  return os.path.join(GetProjectRootPath(), 'data', 'tmp', sub_dir)


def ReadData(filepath: str) -> str:
  """Reads a data file."""
  filepath_full = os.path.join(GetDataDirPath(), filepath)
  return open(filepath_full).read()


def WriteData(filepath: str, content: str) -> None:
  """Writes to a data file.

  Args:
    filepath: the relative path of the file. Subdirectories will be created.
    content: the content to write to the file.
  """
  filepath_full = os.path.join(GetTmpDirPath(), filepath)
  directory = os.path.dirname(filepath_full)
  os.makedirs(directory, exist_ok=True)
  open(filepath_full, 'w').write(content)


def ReadByteData(filepath: str) -> bytes:
  """Reads a bytes data file."""
  filepath_full = os.path.join(GetDataDirPath(), filepath)
  return open(filepath_full, 'rb').read()


def WriteByteData(filepath: str, content: bytes) -> None:
  """Writes bytes to a data file.

  Args:
    filepath: the relative path of the file. Subdirectories will be created.
    content: the content to write to the file.
  """
  filepath_full = os.path.join(GetTmpDirPath(), filepath)
  directory = os.path.dirname(filepath_full)
  os.makedirs(directory, exist_ok=True)
  open(filepath_full, 'wb').write(content)
