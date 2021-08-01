from .base import Base
__all__ = ('Quote', )


class Quote(Base):
    __slots__ = ('level', 'timestamp', 'btc', 'eur', 'usd', 'cny', 'jpy', 'krw', 'eth')

    def __init__(self, level, timestamp, btc, eur, usd, cny, jpy, krw, eth):
        self.level = level
        self.timestamp = timestamp
        self.btc = btc
        self.eur = eur
        self.usd = usd
        self.cny = cny
        self.jpy = jpy
        self.krw = krw
        self.eth = eth

    def __repr__(self):
        return '<%s %s level=%r, timestamp=%r, usd=%r>' % (self.__class__.__name__, id(self), self.level, self.timestamp, self.usd)

    @classmethod
    def from_api(cls, data):
        data = super(Quote, cls).from_api(data)
        level = data['level']
        timestamp = data['timestamp']
        btc = data['btc']
        eur = data['eur']
        usd = data['usd']
        cny = data['cny']
        jpy = data['jpy']
        krw = data['krw']
        eth = data['eth']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        return cls(level, timestamp, btc, eur, usd, cny, jpy, krw, eth)

    @classmethod
    def last(cls, **kwargs):
        """
        Returns last known quote.

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Quote

        Example:
            >>> quote = Quote.last()
        """
        path = 'v1/quotes/last'
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of quotes aligned with blocks.

        Keyword Parameters:
            level (int):  Filters quotes by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters quotes by timestamp. Supports standard modifiers.
            sort (str):  Sorts quotes by specified field. Supported fields: level (default).  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list:  Quotes meeting the specified criteria

        Example:
            >>> quotes = Quote.get(level__gt=150000)
        """
        path = 'v1/quotes'
        optional_base_params = ['level', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of quotes aligned with blocks.

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Example:
            >>> quote_count = Quote.count()
        """
        path = 'v1/quotes/count'
        response = cls._request(path, **kwargs)
        value = response.content
        return int(value)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Fetch latest Quote')
    parser.add_argument('-d', '--domain', type=str, default=Quote.domain, help='tzKT domain to fetch data from')
    args = parser.parse_args()

    quote = Quote.last(domain=args.domain)
    table_format = '{:<10} {:<22} {:<20} {:<20}'
    print(table_format.format('Level', 'Timestamp', 'USD', 'EUR'))
    message = table_format.format(quote.level, quote.timestamp.strftime('%Y-%m-%d %H:%M:%S'), quote.usd, quote.eur)
    print(message)
