"""Unit tests for controlled_market_lib.py"""

import datetime

from absl.testing import absltest

from analysis.trading.simulated_evaluation import controlled_market_lib


class TestStockMetadata(absltest.TestCase):
  """Tests functions in StockMetadata."""

  def setUp(self):
    self.start_dt = datetime.datetime(year=2015, month=1, day=1)
    self.end_dt = datetime.datetime(year=2017, month=1, day=1)
    self.init_price = 1000.0
    self.expected_final_price = 4000.0  # doubles every year

    self.metadata = controlled_market_lib.StockMetadata(
      self.start_dt,
      self.end_dt,
      self.init_price,
      expected_final_price=self.expected_final_price)

  def testExpectedDailyChange(self):
    # 3000 / (2 * 365) = 4.109589041095891
    self.assertAlmostEqual(4.1, self.metadata.expected_daily_change, delta=0.01)

  def testNumDays(self):
    self.assertEqual(365 * 2 + 2, self.metadata.num_days)

  def testNumYears(self):
    self.assertAlmostEqual(2, self.metadata.num_years, delta=0.1)

  def testNumMonths(self):
    self.assertAlmostEqual(24, self.metadata.num_months, delta=0.1)

  def testDailyReturnRate(self):
    # 1.0019 ** 365 = 1.9993897486493237
    self.assertAlmostEqual(
      0.0019, self.metadata.expected_daily_return_rate, delta=0.0001)

  def testMonthlyReturnRate(self):
    # 1.06 ** 12 = 2.012
    self.assertAlmostEqual(
      0.06, self.metadata.expected_monthly_return_rate, delta=0.001)

  def testAnnualReturnRate(self):
    self.assertAlmostEqual(
      1, self.metadata.expected_annual_return_rate, delta=0.1)

  def testOverallReturnRate(self):
    self.assertAlmostEqual(3, self.metadata.expected_overall_return_rate)


class TestStockMetadataConstructors(absltest.TestCase):
  """Tests other constructors in StockMetadata."""

  def testUsingExpectedDailyChange(self):
    start_dt = datetime.datetime(year=2015, month=1, day=1)
    end_dt = datetime.datetime(year=2015, month=1, day=10)
    init_price = 1000.0

    metadata = controlled_market_lib.StockMetadata(
      start_dt,
      end_dt,
      init_price,
      expected_daily_change=5)

    # After 10 days the price will be 1050.
    self.assertAlmostEqual(1050, metadata.expected_final_price)


if __name__ == '__main__':
  absltest.main()
