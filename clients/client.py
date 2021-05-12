from __future__ import annotations
from urllib.parse import ParseResult, urlparse
from core.coingecko import EthPriceFetcher

class Client:
  endpoint: ParseResult
  name: str
  ethPriceFetcher: EthPriceFetcher

  def __init__(self, endpoint: str) -> None:
    self.endpoint = urlparse(endpoint)
    self.ethPriceFetcher = EthPriceFetcher.get_instance()

  def validator_balance(self, epoch: int, public_key: str) -> tuple[int, float]:
    raise NotImplementedError("should be called from subclass")
