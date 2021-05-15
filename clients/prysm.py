from core.constants import GWEI_PER_ETH
from urllib.parse import urljoin
import base64
import logging
import requests
from clients.client import Client

PRYSM_ENDPOINTS = {
  "validator_balance": "/eth/v1alpha1/validators/balances"
}

class PrysmClient(Client):
  def __init__(self, endpoint: str = "http://localhost:3500") -> None:
    super().__init__(endpoint)
    self.name = "prysm"

  def validator_balance(self, epoch: int, public_key: str):
    if epoch < 0:
      raise Exception("Epoch must be positive")
    logging.info("Fetching validator balance for {} at epoch {}...".format(public_key, epoch))

    parsed_key = public_key.replace("0x", "")
    as_b64 = base64.b64encode(bytes.fromhex(parsed_key)).decode("utf-8")
    r = requests.get(self.endpoint.geturl() + PRYSM_ENDPOINTS["validator_balance"], params={
      "epoch": epoch,
      "public_keys": [as_b64],
    })
    res = r.json().get("balances")[0]

    balance = int(res.get("balance")) / GWEI_PER_ETH

    return balance, self.eth_price_at_epoch(epoch)
