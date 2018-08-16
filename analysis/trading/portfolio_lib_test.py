"""Tests for portfolio_lib."""

import datetime
import unittest
from unittest import mock

from analysis.trading import market_lib
from analysis.trading import portfolio_lib


class PortfolioTest(unittest.TestCase):
  def setUp(self):
    self.y1999 = datetime.datetime(1999, 1, 1)
    self.y2000 = datetime.datetime(2000, 1, 1)
    self.y2001 = datetime.datetime(2001, 1, 1)

    def MockPrice(_, dt: datetime.datetime) -> float:
      if dt < datetime.datetime(2000, 6, 1):
        return 1
      else:
        return 10

    self.mock_market = mock.MagicMock(market_lib.Market)
    self.mock_market.GetPriceByDatetime.side_effect = MockPrice

    self.portfolio = portfolio_lib.Portfolio(self.mock_market, self.y1999, 1000)

  def testAdvanceDatetime(self):
    self.assertEqual(self.y1999, self.portfolio.GetCurrentDatetime())
    self.portfolio.AdvanceDatetime(self.y2001)
    self.assertEqual(self.y2001, self.portfolio.GetCurrentDatetime())

  def testBuy(self):
    self.portfolio.MakeTransaction('AAA', 10)

    self.assertEqual(10, self.portfolio.GetShares()['AAA'])
    self.assertEqual(990, self.portfolio.GetFund())

  def testBuyLaterAtDifferentPrice(self):
    self.portfolio.MakeTransaction('AAA', 10, transaction_datetime=self.y2001)

    self.assertEqual(10, self.portfolio.GetShares()['AAA'])
    self.assertEqual(900, self.portfolio.GetFund())

  def testBuyAll(self):
    self.portfolio.BuyAll('AAA')

    self.assertEqual(1000, self.portfolio.GetShares()['AAA'])
    self.assertEqual(0, self.portfolio.GetFund())

  def testSell(self):
    self.portfolio.MakeTransaction('AAA', 10)
    self.portfolio.MakeTransaction('AAA', -5)

    self.assertEqual(5, self.portfolio.GetShares()['AAA'])
    self.assertEqual(995, self.portfolio.GetFund())

  def testSellLaterAtDifferentPrice(self):
    self.portfolio.MakeTransaction('AAA', 10)
    self.portfolio.MakeTransaction('AAA', -5, transaction_datetime=self.y2001)

    self.assertEqual(5, self.portfolio.GetShares()['AAA'])
    self.assertEqual(990 + 50, self.portfolio.GetFund())

  def testSellAll(self):
    self.portfolio.MakeTransaction('AAA', 10)
    self.portfolio.SellAll('AAA')

    self.assertEqual(0, self.portfolio.GetShares()['AAA'])
    self.assertEqual(1000, self.portfolio.GetFund())

  def testMakeTransactionAdvancesDatetime(self):
    self.portfolio.MakeTransaction('AAA', 5, self.y2000)

    self.assertEqual(self.y2000, self.portfolio.GetCurrentDatetime())


if __name__ == '__main__':
  unittest.main()
