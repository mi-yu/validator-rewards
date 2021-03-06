from core.constants import GENESIS_TIMESTAMP, SECONDS_PER_SLOT, SLOTS_PER_EPOCH
from math import ceil
from datetime import datetime

def timestamp_to_eth2_epoch(timestamp: int) -> int:
  return ceil((timestamp - GENESIS_TIMESTAMP) / SECONDS_PER_SLOT / SLOTS_PER_EPOCH)

def eth2_epoch_to_timestamp(epoch: int) -> int:
  return (epoch * SLOTS_PER_EPOCH * SECONDS_PER_SLOT) + GENESIS_TIMESTAMP

def eth2_epoch_to_db_date(epoch: int, fmt: str) -> int:
  return datetime.fromtimestamp(eth2_epoch_to_timestamp(epoch)).strftime(fmt)