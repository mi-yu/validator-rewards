from __future__ import annotations
import logging

from pycoingecko import CoinGeckoAPI

class EthPriceFetcher:
  cg: CoinGeckoAPI
  cache: dict
  __instance: EthPriceFetcher = None

  def __init__(self) -> None:
    if EthPriceFetcher.__instance is not None:
      raise Exception("EthPriceFetcher is a singleton")

    self.cg = CoinGeckoAPI()
    self.cache = {}
    EthPriceFetcher.__instance = self

  @staticmethod
  def get_instance():
    if EthPriceFetcher.__instance is None:
      EthPriceFetcher()
    return EthPriceFetcher.__instance

  def get_eth_usd_price_on_day(self, date: str) -> float:
    try:
      if date in self.cache:
        return self.cache[date]
      res = self.cg.get_coin_history_by_id("ethereum", date)
      price = res["market_data"]["current_price"]["usd"]
      self.cache[date] = price
      return price
    except Exception as e:
      logging.error(e)
      return 0
