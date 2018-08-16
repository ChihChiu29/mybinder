"""Improved ChromeDriver.

ONLY opens one chromedriver at a time; using multiple chromedriver in several
processes will not go pretty.
"""

import subprocess
import time

import retrying
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver

from tool import settings
from tool import t

_KILLING_NUM_RETRIES = 5
_GET_URL_NUM_RETRIES = 5
_SLEEP_BETWEEN_RETRIES = 0.5
_KILL_CHROME_BEFORE_RETRY = False


def _RetryOnException(exception: Exception) -> bool:
  return isinstance(exception, WebDriverException)


class ChromeDriverManager(object):
  """Manage Chrome WebDriver so actions can be retried."""

  def __init__(self):
    self._driver = None

  @retrying.retry(
    retry_on_exception=_RetryOnException,
    stop_max_attempt_number=_GET_URL_NUM_RETRIES,
    wait_fixed=_SLEEP_BETWEEN_RETRIES)
  def Do(self, action_fn: t.Callable[[WebDriver], t.T]) -> t.T:
    """Performs actions using provided WebDriver.

    Wrap actions you want to perform into action_fn, and make sure these actions
    start with one that sets the state (e.g. load an url). When there is a crash
    for chromedriver which makes any of the actions to fail, a new chromedriver
    will be created and action_fn will be retried. Do *NOT* assume any state
    from previous calls of this function, always assume you might start with
    a new browser.

    If chromedriver does not crash, the save driver is reused cross multiple
    calls of this function. If you do want to start with a new chromedriver
    (which starts a new chrome window with new session), use the Quit function
    to close the existing chromedriver.
    """
    driver = self._GetOrCreateDriver()
    try:
      return action_fn(driver)
    except Exception as e:
      if _KILL_CHROME_BEFORE_RETRY:
        _KillChromesAndDrivers()
      self._driver = None
      raise e

  def Quit(self):
    """Quits the created WebDriver."""
    try:
      self._driver.quit()
    except Exception:
      pass
    self._driver = None

  def _GetOrCreateDriver(self):
    if not self._driver:
      if settings.RunInDocker():
        self._driver = _CreateChromeDriverForDocker()
      else:
        self._driver = webdriver.Chrome()
    return self._driver


def _KillChromesAndDrivers():
  # It's best effort killing, since defunct chromedriver attached to the current
  # process won't die until the program quits.
  for _ in range(_KILLING_NUM_RETRIES + 1):
    existing_process = subprocess.check_output(
      'echo $(ps -e | grep chrome)', shell=True)
    if existing_process == '\n':
      return
    subprocess.call(['killall', '-KILL', '-r', 'chrome'])
    time.sleep(_SLEEP_BETWEEN_RETRIES)


def _CreateChromeDriverForDocker() -> WebDriver:
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  options.add_argument('--disable-gpu')
  options.add_argument('--no-sandbox')
  return webdriver.Chrome(chrome_options=options)
