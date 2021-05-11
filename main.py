import argparse
from core.validator import Validator

if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  parser.add_argument("--client-type", type=str)
  parser.add_argument("--beacon-chain-endpoint", type=str)
  parser.add_argument("--public-keys", type=str, nargs="+", default=[])
  parser.add_argument("--indices", type=str, nargs="+", default=[])

  args = parser.parse_args()

  validators = [Validator(key, args.beacon_chain_endpoint, args.client_type) for key in args.public_keys]

  for v in validators:
    print(v.balance_at_epoch(35174))

