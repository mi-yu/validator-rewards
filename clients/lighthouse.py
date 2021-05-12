import logging

import requests
from core.constants import SLOTS_PER_EPOCH
from clients.client import Client

LIGHTHOUSE_ENDPOINTS = {
  "validator_balances": "/eth/v1/beacon/states/{}/validator_balances"
}

class LighthouseClient(Client):
  def __init__(self, endpoint: str = "http://localhost:5052") -> None:
    super().__init__(endpoint)
    self.name = "lighthouse"

  def validator_balance(self, epoch: int, public_key: str):
    if epoch < 0:
      raise Exception("Epoch must be positive")

    slot_no = epoch * SLOTS_PER_EPOCH
    retries = 5
    logging.info("Fetching validator balance for {} at epoch {}...".format(public_key, epoch))

    while retries != 0:
      r = requests.get(self.endpoint.geturl() + LIGHTHOUSE_ENDPOINTS["validator_balances"].format(str(slot_no)), params={
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

    return data[0].get("balance")
