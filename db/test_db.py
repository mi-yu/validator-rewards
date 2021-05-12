from localdb import SQLiteDB

if __name__ == '__main__':
    db = SQLiteDB('test.db')
    test_obj_1 = {
        'key': 'eth2hash',
        'estimated_timestamp': '2021-05-10',
        'epoch': '102',
        'eth_balance': '43.21',
        'hist_usd_per_eth': '12.34',
        'hist_usd_value': '1204.23'
    }
    test_obj_2 = {
        'key': 'eth2hash',
        'estimated_timestamp': '2021-05-11',
        'epoch': '57',
        'eth_balance': '43.21',
        'hist_usd_per_eth': '12.34',
        'hist_usd_value': '1204.23'
    }
    db.save([test_obj_1, test_obj_2])
    print(db.load_view('eth2hash', '2021-05-09', '2021-05-10'))
    print(db.last_saved('eth2hash'))