# Eth 2 Validator Rewards

## Installation

1. If you do not have `pipenv` installed, install it here: https://pypi.org/project/pipenv/
2. Clone this repo and in the project root run `pipenv install`
3. Then run `pipenv shell`

## Usage

In the `pipenv` shell run:

```
python main.py <options>
```

The following options are available


| Option      | Description |
| ----------- | ----------- |
| `--public-keys` (required)      | space separated list of public keys, ex: `0x8001ffc81a8be963f40e418fe780b1c065f0a6d811a0f777bd2a77f9eeacb2f7bd47468dfebf8c0d574e49de53b94b29`      |
| `--client-type` (required)   | one of `infura`, `lighthouse`, or `prysm`        |
| `--beacon-node-endpoint` (required)   | endpoint (and port if applicable) of beacon node, ex: `http://localhost:3500` for Prysm       |
| `--start-date` (required)   | first date to fetch data for in YYYY-MM-dd format, ex: `2021-05-01`    |
| `--end-date` (required)   | last date to fetch data for in YYYY-MM-dd format, ex: `2021-05-15`    |
| `--db-path`   | specify path for SQLite db file, defaults to `rewards.db`  |

Example for Lighthouse:

```
python main.py \
  --public-keys 0x8001ffc81a8be963f40e418fe780b1c065f0a6d811a0f777bd2a77f9eeacb2f7bd47468dfebf8c0d574e49de53b94b29 \
  --client-type lighthouse \
  --beacon-chain-endpoint http://localhost:5052 \
  --start-date 2020-12-02 \
  --end-date 2020-12-0
```
