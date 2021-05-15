import argparse
from datetime import datetime
import sys
import csv
import logging
from core.validator import Validator
from utils.time import eth2_epoch_to_db_date
# from db.db import DB_DEFAULT_DT_FMT
from db.localdb import SQLiteDB
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
  start = datetime.now()
  parser = argparse.ArgumentParser()

  parser.add_argument("--client-type", type=str)
  parser.add_argument("--beacon-chain-endpoint", type=str)
  parser.add_argument("--public-keys", type=str, nargs="+", default=[])
  parser.add_argument("--indices", type=str, nargs="+", default=[])
  parser.add_argument("--start-date", type=str, required=True)
  parser.add_argument("--end-date", type=str, required=True)
  parser.add_argument("--concurrency", type=int, default=5)
  parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
  parser.add_argument("-o", "--output-file", type=str)
  parser.add_argument("-t", "--timing", action="store_true")
  args = parser.parse_args()

  if args.verbose:
    logging.basicConfig(level=logging.INFO)

  validators = [Validator(key, args.beacon_chain_endpoint, args.client_type, args.concurrency) for key in args.public_keys]
  db = SQLiteDB('rewards.db')

  for v in validators:
    response = v.balances_at_dates(args.start_date, args.end_date, db)
    save_data = [{'epoch': ep, \
                  'eth_balance': bal, \
                  'hist_usd_per_eth': price, \
                  'hist_usd_value': price * bal, \
                  'estimated_timestamp': eth2_epoch_to_db_date(ep, db.time_fmt), \
                  'key': v.public_key} for ep, bal, price in response]
    db.save(save_data)

  handle = open(args.output_file, "w") if args.output_file else sys.stdout
  with handle as f:
    writer = csv.writer(f)
    writer.writerow(["public_key", "date", "eth_balance", "usd_eth_price", "usd_value"])
    start_ts = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_ts = datetime.strptime(args.end_date, "%Y-%m-%d")
    for v in validators:
      data = db.load_view(v.public_key, start_ts, end_ts)
      for row in data:
        writer.writerow([v.public_key] + list(row))

  elapsed = datetime.now().timestamp() - start.timestamp()
  if args.timing:
    print(elapsed)

