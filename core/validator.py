from __future__ import annotations
import requests
import logging
from clients.client import Client
from clients.infura import InfuraClient
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
  },
  "infura": {
    "constructor": InfuraClient,
  }
}


def new_client_from_name(name: str) -> Client:
  config = CLIENT_DEFAULTS.get("name")
  if config is None:
    logging.error("No client named {}".format(name))
    raise Exception("No client named {}".format(name))

  return config["constructor"]()

class Validator:
  public_key: str
  client: Client

  def __init__(self, public_key: str, beacon_chain_endpoint: str = None, client_type: str = None) -> None:
    self.public_key = public_key

    if beacon_chain_endpoint is None:
      self.client = self._autodetect_beaconchain_client()
    elif client_type == "infura":
      self.client = InfuraClient(beacon_chain_endpoint)
    elif client_type == "lighthouse":
      self.client = LighthouseClient(beacon_chain_endpoint)
    elif client_type == "prysm":
      self.client = PrysmClient(beacon_chain_endpoint)
    else:
      raise Exception("Invalid client_type {}".format(client_type))

  def _autodetect_beaconchain_client(self) -> Client:
    connect_to = None
    for client, config in CLIENT_DEFAULTS.items():
      if client == "infura":
        continue

      try:
        r = requests.get(config.get("endpoint") + config.get("test_path"))
        if r.status_code == 200:
          connect_to = client
          break
        else:
          raise Exception()
      except Exception:
        logging.info("Failed to connect to beacon chain client {} at {}, trying next client".format(client, config.get("endpoint")))

    if connect_to is None:
      logging.error("Unable to find a beacon chain client to connect to, try specifying an endpoint with the --beacon-chain-endpoint option")
      return None
    if connect_to not in CLIENT_DEFAULTS:
      logging.error("Client {} does not exist in default client config, possible options are {}".format(connect_to, list(CLIENT_DEFAULTS.keys())))
      return None

    return new_client_from_name(connect_to)

  def balance_at_epoch(self, epoch: int) -> int:
    return self.client.validator_balance(epoch, self.public_key)

