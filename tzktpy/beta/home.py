from tzktpy.base import Base


def summary(**kwargs):
    """
    Fetches high-level data about the current state of the Tezos network.

    Keyword Parameters:
        quote (str, optional):  The currency to denominate financial values in.  Defaults to 'usd'.
        domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

    Returns:
        dict: Miscellaneous high-level data about the current state of Tezos network.

    Examples:
        >>> quote = 'btc'
        >>> data = home(quote=quote)
    """
    path = 'v1/home'
    quote = kwargs.pop('quote', 'usd')
    params = dict(quote=quote)
    response = Base._request(path, params=params, **kwargs)
    return response.json()


def blocks(**kwargs):
    """
    Fetches high-level data about the latest blocks added to the Tezos network.

    Keyword Parameters:
        domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

    Returns:
        dict: Miscellaneous high-level data about the latest blocks added to the Tezos network.

    Examples:
        >>> data = blocks(quote=quote)
    """
    path = 'v1/home/blocks'
    response = Base._request(path, **kwargs)
    return response.json()


class Asset(Base):
    __slots__ = ('address', 'alias', 'balance', 'num_transactions', 'first_activity_time', 'last_activity_time', 'creator', 'tzips')

    def __init__(self, address, alias, balance, num_transactions, first_activity_time, last_activity_time, creator, tzips):
        self.address = address
        self.alias = alias
        self.balance = balance
        self.num_transactions = num_transactions
        self.first_activity_time = first_activity_time
        self.last_activity_time = last_activity_time
        self.tzips = tzips

    def __str__(self):
        return self.address

    def __repr__(self):
        return '<%s %s address=%r, alias=%r, balance=%r, num_transactions=%r>' % (self.__class__.__name__, id(self), self.address, self.alias, self.balance, self.num_transactions)

    @classmethod
    def from_api(cls, data):
        address = data['address']
        alias = data['alias']
        balance = data['balance']
        num_transactions = data['numTransactions']
        first_activity_time = data['firstActivityTime']
        last_activity_time = data['lastActivityTime']
        creator = data['creator']
        tzips = data['tzips']
        return cls(address, alias, balance, num_transactions, first_activity_time, last_activity_time, creator, tzips)

    @classmethod
    def top(cls, **kwargs):
        """
        Fetches high-level data about the top assets on the Tezos network.

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            dict: Miscellaneous high-level data about the top assets  on the Tezos network.

        Examples:
            >>> data = Asset.top()
        """
        path = 'v1/home/assets'
        response = cls._request(path, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]


def top_accounts(**kwargs):
    """
    Fetches high-level data about the top accounts on the Tezos network.

    Keyword Parameters:
        domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

    Returns:
        dict: Miscellaneous high-level data about the top accounts on the Tezos network.

    Examples:
        >>> data = top_accounts()
    """
    path = 'v1/home/accounts'
    response = Base._request(path, **kwargs)
    return response.json()


def top_bakers(**kwargs):
    """
    Fetches high-level data about the top bakers on the Tezos network.

    Keyword Parameters:
        domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

    Returns:
        dict: Miscellaneous high-level data about the top bakers on the Tezos network.

    Examples:
        >>> data = top_bakers()
    """
    path = 'v1/home/bakers'
    response = Base._request(path, **kwargs)
    return response.json()
