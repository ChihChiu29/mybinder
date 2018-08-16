"""Fetches stocks info from Alpha Vantage."""
import json

from absl import flags, app

from tool import file
from tool import nbshttp
from tool import t

FLAGS = flags.FLAGS

flags.DEFINE_string(
  'symbol', 'GOOG',
  'The symbol of the stocks to fetch.')

flags.DEFINE_string(
  'save_filepath', 'google_alphavantage.json',
  'Save data to this file/path.')

flags.DEFINE_bool(
  'compact', False,
  'Whether only fetch for last 100 days.')


class Client:
  url_template = (
    'https://www.alphavantage.co/query'
    '?function=TIME_SERIES_DAILY'
    '&symbol={symbol}'
    '&outputsize={compact_or_full}'
    '&apikey={api_key}')
  api_key = 'I9XIWDM97Z0LU2K0'

  def FetchStockPrice(self, symbol: str, is_compact: bool = True) -> t.JSON:
    """Fetch stock price.

    Args:
      symbol (string): the symbol of the stock, like "GOOG".
      is_compact (bool): whether the search is for the last 100 data points (
          compact) or full history.

    Returns:
      string: JSON for the daily stock price.
    """
    url = self.url_template.format(
      symbol=symbol,
      compact_or_full='compact' if is_compact else 'full',
      api_key=self.api_key,
    )
    return nbshttp.JsonGET(url)


def main(_):
  client = Client()
  file.WriteData(
    FLAGS.save_filepath,
    json.dumps(client.FetchStockPrice(FLAGS.symbol, is_compact=FLAGS.compact)))


if __name__ == '__main__':
  app.run(main)
