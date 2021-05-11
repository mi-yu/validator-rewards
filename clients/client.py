from __future__ import annotations
from typing import Any
import logging
import requests
from urllib.parse import urljoin, ParseResult, urlparse

from clients.lighthouse import LighthouseClient
from clients.prysm import PrysmClient

CLIENT_DEFAULTS = {
  "prysm": {
    "endpoint": "http://localhost:3500",
    "test_path": "/eth/v1/node/version",
    "constructor": PrysmClient,
  },
  "lighthouse": {
    "endpoint": "http://localhost:5052",
    "test_path": "/eth/v1alpha1/beacon/chainhead",
    "constructor": LighthouseClient
  }
}

class Client:
  endpoint: ParseResult
  name: str

  def __init__(self, endpoint: str) -> None:
    self.endpoint = urlparse(endpoint)

  @staticmethod
  def new_client_from_name(name: str) -> Client:
    config = CLIENT_DEFAULTS.get("name")
    if config is None:
      logging.error("No client named {}".format(name))
      raise Exception("No client named {}".format(name))

    return config["constructor"]()

  def validator_balance(self, epoch: int):
    raise NotImplementedError("should be called from subclass")
