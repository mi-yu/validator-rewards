from core.constants import GENESIS_TIMESTAMP, SECONDS_PER_SLOT, SLOTS_PER_EPOCH
from math import ceil

def timestamp_to_eth2_epoch(timestamp: int) -> int:
  return ceil((timestamp - GENESIS_TIMESTAMP) / SECONDS_PER_SLOT / SLOTS_PER_EPOCH)