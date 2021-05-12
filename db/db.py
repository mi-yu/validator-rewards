from schema import Schema, Use, And
from datetime import datetime

def _validate_date(date_text: str) -> bool:
    try:
        datetime.strptime(date_text, DB_DEFAULT_DT_FMT)
        return True
    except ValueError:
        return False

# TODO: maybe a config to configure database schema + DT Format
DB_DEFAULT_SCHEMA = {
    'epoch': Use(int),
    'estimated_timestamp': And(Use(str), _validate_date),
    'eth_balance': Use(float),
    'hist_usd_per_eth': Use(float),
    'hist_usd_value': Use(float)
}

DB_DEFAULT_DT_FMT = '%Y-%m-%d'

class DB():
    # Location can either be a file path or some other network endpoint
    def __init__(self, location: str, config = None):
        self.location = location
        if config == None:
            self.schema = Schema(DB_DEFAULT_SCHEMA)
            self.fields = DB_DEFAULT_SCHEMA.keys()

    def header(self):
        return tuple(self.fields)

    def save(self, key, data) -> None:
        raise NotImplementedError('Call my Subclass')

    def load_view(self, key, start, end):
        raise NotImplementedError('Call my subclass')

    def last_saved(self, key):
        raise NotImplementedError('Call my subclass')