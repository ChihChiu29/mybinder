"""Download and save stocks data files."""

from absl import app
from absl import flags

from datacollection.finance import alpha_vantage as alpha_vantage_client
from datacollection.processor import alpha_vantage as alpha_vantage_processor
from tool import file

FLAGS = flags.FLAGS

# Examples: ['GOOG', 'AAPL', 'AMZN', 'MSFT', 'TSLA', 'FB']
flags.DEFINE_multi_string(
  'symbols', [],
  'The symbol(s) to fetch for.')


def DownloadStockData(symbol: str):
  """Downloads and saves stock data to a pickle file."""
  client = alpha_vantage_client.Client()
  stocks_json = client.FetchStockPrice(symbol, is_compact=False)

  reader = alpha_vantage_processor.PriceJsonReader()
  reader.ReadJson(stocks_json)
  file.WriteByteData('stocks/%s.pickle' % symbol, reader.ToPickle())


def main(_):
  for symbol in FLAGS.symbols:
    DownloadStockData(symbol)


if __name__ == '__main__':
  app.run(main)
