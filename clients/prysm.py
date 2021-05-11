from urllib.parse import urljoin, urlparse

import requests
from clients.client import Client

PRYSM_ENDPOINTS = {
  "validator_balance": "/eth/v1alpha1/validators/balances"
}

class PrysmClient(Client):
  def __init__(self, endpoint: str = "http://localhost:3500") -> None:
    super().__init__(endpoint)
    self.name = "prysm"

  def validator_balance(self, epoch: int):
    r = requests.get(str(urljoin(self.endpoint + PRYSM_ENDPOINTS["validator_balance"])), params={
      "epoch": epoch
    })
    return r.json()
