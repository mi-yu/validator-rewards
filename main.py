import argparse
import logging
from core.validator import Validator
from utils.time import eth2_epoch_to_db_date
from db.db import DB_DEFAULT_DT_FMT
from db.localdb import SQLiteDB
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  parser.add_argument("--client-type", type=str)
  parser.add_argument("--beacon-chain-endpoint", type=str)
  parser.add_argument("--public-keys", type=str, nargs="+", default=[])
  parser.add_argument("--indices", type=str, nargs="+", default=[])
  parser.add_argument("--start-date", type=str, required=True)
  parser.add_argument("--end-date", type=str, required=True)
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
  args = parser.parse_args()

  if args.verbose:
    logging.basicConfig(level=logging.INFO)

  validators = [Validator(key, args.beacon_chain_endpoint, args.client_type) for key in args.public_keys]
  db = SQLiteDB('rewards.db')

  for v in validators:
    response = v.balances_at_dates(args.start_date, args.end_date)
    save_data = [{'epoch': ep, \
                  'eth_balance': bal, \
                  'hist_usd_per_eth': price, \
                  'hist_usd_value': price * bal, \
                  'estimated_timestamp': eth2_epoch_to_db_date(ep, DB_DEFAULT_DT_FMT), \
                  'key': v.public_key[2:]} for ep, bal, price in response]
    db.save(save_data)
