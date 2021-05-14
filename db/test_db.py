from localdb import SQLiteDB

if __name__ == '__main__':
    db = SQLiteDB('test.db')
    test_key = '0x8001ffc81a8be963f40e418fe780b1c065f0a6d811a0f777bd2a77f9eeacb2f7bd47468dfebf8c0d574e49de53b94b29'
    test_obj_1 = {
        'key': test_key,
        'estimated_timestamp': '2021-05-10',
        'epoch': '102',
        'eth_balance': '43.21',
        'hist_usd_per_eth': '12.34',
        'hist_usd_value': '1204.23'
    }
    test_obj_2 = {
        'key': test_key,
        'estimated_timestamp': '2021-05-11',
        'epoch': '57',
        'eth_balance': '43.21',
        'hist_usd_per_eth': '12.34',
        'hist_usd_value': '1204.23'
    }
    db.save([test_obj_1, test_obj_2])
    print(db.load_view(test_key, '2021-05-09', '2021-05-10'))
    print(db.last_saved(test_key))
    print(db.is_processed(test_key, '2021-05-09'))
    print(db.is_processed(test_key, '2021-05-11'))