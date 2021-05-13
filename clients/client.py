from __future__ import annotations
from datetime import datetime
from urllib.parse import ParseResult, urlparse
from utils.time import eth2_epoch_to_timestamp
from core.coingecko import EthPriceFetcher

class Client:
  endpoint: ParseResult
  name: str
  ethPriceFetcher: EthPriceFetcher

  def __init__(self, endpoint: str) -> None:
    self.endpoint = urlparse(endpoint)
    self.ethPriceFetcher = EthPriceFetcher.get_instance()

  def eth_price_at_epoch(self, epoch: int) -> float:
    date = datetime.fromtimestamp(eth2_epoch_to_timestamp(epoch)).strftime("%d-%m-%Y")
    price = self.ethPriceFetcher.get_eth_usd_price_on_day(date)
    return price

  def validator_balance(self, epoch: int, public_key: str) -> tuple[int, float]:
    raise NotImplementedError("should be called from subclass")
