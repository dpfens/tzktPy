# tzktPy
A Python wrapper for the tzKT API

## Install
To install `tzktpy` execute the following commands:
```bash
git clone git@github.com:dpfens/tzktPy.git
cd tzktPy
python setup.py install
```

## Usage
```python
import tzktpy as tzkt

address = 'tz...'
account = tzkt.account.Account.by_address(address)
```

```python
```

## Scripts
tzktPy comes with a few executable scripts for simple/common tasks:

*  `account` - Fetches the balance of the given account addresses
*  `balance` - Fetches the balance history of the given account
*  `block` - Fetches the designated block and associated information
*  `head` - Fetches the current head of the blockchain
*  `protocol` - Fetches the current protocol
*  `quote` - Fetches the current price of a Tez in USD and EUR.
*  `reward` - Fetches the rewards given to a baker/delegator
*  `software` - Lists the different versions of software used on the blockchain
*  `statistics` - Fetch statistics for a given date/cycle
*  `voting` - Fetches the current state of the proposal votes and the voters

These scripts all in the following format:
```bash
python -m tzktpy.account <arguments>
python -m tzktpy.balance <arguments>
python -m tzktpy.balance <arguments>
```
