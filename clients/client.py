from __future__ import annotations
from urllib.parse import ParseResult, urlparse


class Client:
  endpoint: ParseResult
  name: str

  def __init__(self, endpoint: str) -> None:
    self.endpoint = urlparse(endpoint)

  def validator_balance(self, epoch: int, public_key: str):
    raise NotImplementedError("should be called from subclass")
