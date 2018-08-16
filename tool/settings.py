"""Global settings and related helper functions."""
import os


def RunInDocker() -> bool:
  """If the current program runs in a Docker container."""
  return os.path.exists('/.dockerenv')
