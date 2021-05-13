from datetime import datetime
import logging
from utils.time import eth2_epoch_to_timestamp
import requests
from clients.client import Client
from core.constants import GWEI_PER_ETH, SLOTS_PER_EPOCH

INFURA_ENDPOINTS = {
  "validator_balances": "/eth/v1/beacon/states/{}/validator_balances"
}

class InfuraClient(Client):
  def __init__(self, endpoint: str) -> None:
    super().__init__(endpoint)
    self.name = "infura"

  def validator_balance(self, epoch: int, public_key: str):
    if epoch < 0:
      raise Exception("Epoch must be positive")

    slot_no = epoch * SLOTS_PER_EPOCH
    retries = 5
    logging.info("Fetching validator balance for {} at epoch {}...".format(public_key, epoch))

    while retries != 0:
      r = requests.get(self.endpoint.geturl() + INFURA_ENDPOINTS["validator_balances"].format(str(slot_no)), params={
        "id": public_key
      })
      if r.status_code == 200:
        break
      retries -= 1
      logging.info("validator_balance request failed with code {}, {} retries left".format(str(r.status_code), str(retries)))

    if retries == 0:
      return 0

    data = r.json().get("data")
    if not data or len(data) != 1:
      logging.info("No validator balance for {} at epoch {}".format(public_key, str(epoch)))
      return 0

    balance = int(data[0].get("balance")) / GWEI_PER_ETH
    usd_value = self.eth_price_at_epoch(epoch) * balance

    return balance, usd_value
