import csv
import db.DB


# Validate fields before writing
class CSVDB(DB):
    def __init__(self, filepath: str):
        super().__init__(filepath)
        self.last_write = None
    
    def save(self, data_entries) -> None:
        with open(self.location, 'w', newline='') as csvfile:
            for data in data_entries:
                fieldnames = self.schema.fields
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(data)

    def load_view(self, key, start, end):
        with open(self.location, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                return row['key']

    def last_saved(self, key):
        return self.last_write