import logging
from urllib.parse import urljoin
import requests
from clients.client import Client
from core.constants import SECONDS_PER_SLOT, SLOTS_PER_EPOCH

INFURA_ENDPOINTS = {
  "validator_balances": "/eth/v1/beacon/states/{}/validator_balances"
}

class InfuraClient(Client):
  def __init__(self, endpoint: str) -> None:
    super().__init__(endpoint)
    self.name = "infura"

  def validator_balance(self, epoch: int, public_key: str):
    slot_no = epoch * SLOTS_PER_EPOCH
    retries = 3

    while retries != 0:
      r = requests.get(self.endpoint.geturl() + INFURA_ENDPOINTS["validator_balances"].format(str(slot_no)), params={
        "id": public_key
      })
      print(r.status_code)
      if r.status_code == 200:
        break
      retries -= 1
      logging.info("validator_balance request failed, {} retries left", retries)

    data = r.json().get("data")
    print(data)
    if not data or len(data) != 1:
      logging.info("No validator balance for {} at epoch {}".format(public_key, epoch))
      return 0

    return data[0].get("balance")
