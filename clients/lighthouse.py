from clients.client import Client

class LighthouseClient(Client):
  def __init__(self, endpoint: str = "http://localhost:5052") -> None:
    super().__init__(endpoint)
    self.name = "lighthouse"

  def validator_balance(self, epoch: int):
    pass