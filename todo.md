# Fetching data
- beacon node's builtin http server (running on localhost)
- can do concurrent requests to speed things up, need to test
- Need to write some abstraction around client type

# Database
- pick a DB (later)
- write to CSV for now
- Things to store (per validator public key)
    - eth_balance
    - historical_usd_value
    - usd_per_eth
    - epoch
    - estimated_timestamp

# Config options
- `--output-file`
- `--start-date`
- `--end-date`
- `--public-keys`
- `--client-type` (prysm, lighthouse, nimbus)


