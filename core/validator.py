from urllib.parse import urlparse
import requests
import logging
from clients.client import Client, CLIENT_DEFAULTS


class Validator:
  index: int
  public_key: str
  client: Client

  def __init__(self, index: int, public_key: str, beacon_chain_endpoint: str = None) -> None:
    self.index = index
    self.public_key = public_key

    if beacon_chain_endpoint is None:
      self.client = self._autodetect_beaconchain_client()
    else:
      self.client = Client(beacon_chain_endpoint)

  def _autodetect_beaconchain_client(self) -> Client:
    connect_to = None
    for client, config in CLIENT_DEFAULTS.items():
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

    return Client.new_client_from_name(connect_to)

