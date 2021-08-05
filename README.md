# tzktPy
A Python wrapper for the tzKT API.  The current implementation supports all methods in version 1.6.0.

## Install
To install `tzktpy` execute the following commands:
```bash
git clone git@github.com:dpfens/tzktPy.git
cd tzktPy
python setup.py install
```

## Scripts
tzktPy comes with a few executable scripts for simple/common tasks:

*  `tzktpy.account` - Fetches the balance of the given account addresses
*  `tzktpy.balance` - Fetches the balance history of the given account
*  `tzktpy.block` - Fetches the designated block and associated information
*  `tzktpy.head` - Fetches the current head of the blockchain
*  `tzktpy.operation` - Fetches transaction operations involving the given account address
*  `tzktpy.protocol` - Fetches the current protocol
*  `tzktpy.quote` - Fetches the current price of a Tez in USD and EUR.
*  `tzktpy.reward` - Fetches the rewards given to a baker/delegator
*  `tzktpy.software` - Lists the different versions of software used on the blockchain
*  `tzktpy.statistics` - Fetch statistics for a given date/cycle
*  `tzktpy.voting` - Fetches the current state of the proposal votes and the voters

These scripts all in the following format:
```bash
python -m tzktpy.head
python -m tzktpy.account <arguments>
python -m tzktpy.balance <arguments>
```

To get a description on how to use the script, use the `--help` argument to get the `argparse` description.

## Quickstart

## Filtering search criteria using modifiers
The tzKT API offers flexible queries to filter objects and filter the number of objects that match a specified criteria.  These criteria use modifiers to specify the type of comparison that should be performed.  These modifiers include the following:

### Standard modifiers
*  `eq` = equal to
*  `ne` = not equal to
*  `gt` = greater than
*  `ge` = greater than or equal to
*  `lt` = less than
*  `le` = less than or equal to
*  `in` = value is in a list of multiple values
*  `ni` = value is not in a list of multiple values

This library supports these modifiers, which need to be provided provided as `<field>__<modifier>` keyword arguments.  This resembles the same notation used in queries in Django.  For example, to fetch all Accounts with balances between `1000` and `100000`, we would use the following command:
```python
import tzktpy as tzkt
tzkt.account.Account.get(balance__ge=1000, balance__lt=100000)
```

### Pagination modifiers
*  `offset`
   *  `el` = elements offset.  Skip specified number of elements
   *  `pg` = page offset. Skip `page * limit` elements.
   *  `cr` = cursor offset.  Skips all elements with the cursor before (including) the specified value. Cursor is a field used for sorting, e.g. `id`. Avoid using this offset mode with non-unique or non-sequential cursors such as `amount`, `balance`, etc.
*  `sort`
   *  `asc` = Specify a field name to sort by ascending.
   *  `desc` = Specify a field name to sort by descending.


To paginate through accounts using a normal `offset`:
```python
limit = 1000
offset = 0
accounts = []
while page:
    page = Account.get(limit=limit, offset=offset)
    offset += limit
    accounts += page
```

To paginate through accounts using the pages modifier (`pg`):
```python
accounts = []
page_number = 0
while page:
    page = Account.get(offset__pg=page_number);
    accounts += page
    page_number += 1
```

Both are valid approaches to pagination using `tzktpy`.  Modifiers are only supported by API endpoints that return multiple objects (`get` methods), and objects that return the total number of a given object (`count` methods).

### Fetching an Account By Address
```python
import tzktpy as tzkt

address = 'tz1WEHHVMWxQUtkWAgrJBFGXjJ5YqZVgfPVE'
account = tzkt.account.Account.by_address(address)
```

### Fetching Accounts by Criteria
```python
import tzktpy as tzkt
# fetch only contract accounts with a balance < 100000
tzkt.account.Account.get(type='contract', balance__lt=100000)
```

### Fetching Operations
Tzkt supports fetching details on operations performed.

#### Fetch all Operations performed on an account
```python
import tzktpy as tzkt
address = 'tz1WEHHVMWxQUtkWAgrJBFGXjJ5YqZVgfPVE'
operations = []
page_number = 0
while page:
    page = Operation.by_address(address, offset__pg=page_number);
    operations += page
    page_number += 1
```

### Fetching Blocks
```python
# by level
import tzktpy as tzkt
block = tzkt.block.Block.by_level(150000)

# by levels between 100000 and 110000
blocks = tzkt.block.Block.get(level__gt=100000, level__lt=110000, limit=10000)
```

## Beta module
The beta module is for API endpoints that may not be permanent fixtures of the tzktpy library.  Endpoints in the beta module may be renamed or removed from the beta module at any time, or may stop working.  Endpoints that become stable will be moved to another module in tzktpy.

## Contributions
Contributions are welcome.  Feel free to submit issues and pull requests.
