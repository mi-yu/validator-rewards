import sqlite3
from db import DB
import logging

# Validate fields before writing
class SQLiteDB(DB):
    def __init__(self, filepath: str):
        super().__init__(filepath)
        self.last_write = {}
        self.conn = sqlite3.connect(self.location)

    
    # data_entries is a list of dictionaries with the field 'key' + whatever the schema requires
    def save(self, data_entries) -> None:
        cur = self.conn.cursor()
        exclude_keys = {'key'}
        for data in data_entries:
            key = data['key']
            save_data = {k: data[k] for k in set(list(data.keys())) - exclude_keys}
            self.schema.validate(save_data)
            
            if not self._key_exists(key):
                header = str(self.header()).replace("'", "")
                cur.execute(f'''CREATE TABLE {key} {header}''')

            values = tuple(save_data[k] for k in self.header())
            cur.execute(f'''INSERT INTO {key} VALUES {values} ''')
            self.conn.commit()

    def _key_exists(self, key: str) -> bool:
        """ This method seems to be working now"""
        query = f"SELECT name from sqlite_master WHERE type='table' AND name='{key}';"
        cursor = self.conn.execute(query)
        result = cursor.fetchone()
        if result == None:
            return False
        else:
            return True 

    def load_view(self, key: str, start: str, end: str, date_col: str = 'estimated_timestamp'):
        if not self._key_exists(key):
            logging.info(f'key not found in db: {key}')
            return None
        else:
            query = f"SELECT * from {key} WHERE {date_col} BETWEEN '{start}' AND '{end}';"
            cursor = self.conn.execute(query)
            return cursor.fetchall()

    def last_saved(self, key, date_col: str = 'estimated_timestamp'):
        if not self._key_exists(key):
            logging.info(f'key not found in db: {key}')
            return None
        else:
            query = f"SELECT * from {key} ORDER BY {date_col} DESC;"
            cursor = self.conn.execute(query)
            return cursor.fetchone()