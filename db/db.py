from schema import Schema

DB_DEFAULTS = {
    'csv': './out/rewards-db.csv'
}

class DB():
    # Location can either be a file path or some other network store
    def __init__(self, location: str):
        self.location = location
        self.schema = None
    def save(self, key, data) -> None:
        raise Exception('Call my Subclass')

    def load_view(self, key, start, end):
        raise Exception('Call my subclass')

    def last_saved(self, key):
        raise Exception('Call my subclass')