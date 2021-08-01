from .base import Base
__all__ = ('Statistics', )


class Statistics(Base):
    __slots__ = ('cycle', 'date', 'level', 'timestamp', 'total_supply', 'circulating_supply', 'total_bootstrapped', 'total_commitments', 'total_activated', 'total_created', 'total_burned', 'total_vested', 'total_frozen', 'quote')

    def __init__(self, cycle, date, level, timestamp, total_supply, circulating_supply, total_bootstrapped, total_commitments, total_activated, total_created, total_burned, total_vested, total_frozen, quote):
        self.cycle = cycle
        self.date = date
        self.level = level
        self.timestamp = timestamp
        self.total_supply = total_supply
        self.circulating_supply = circulating_supply
        self.total_bootstrapped = total_bootstrapped
        self.total_commitments = total_commitments
        self.total_activated = total_activated
        self.total_created = total_created
        self.total_burned = total_burned
        self.total_vested = total_vested
        self.total_frozen = total_frozen
        self.quote = quote

    def __repr__(self):
        return '<%s %s cycle=%r, date=%r, level=%r, timestamp=%r, total_supply=%r, circulating_supply=%r>' % (self.__class__.__name__, id(self), self.cycle, self.date, self.level, self.timestamp, self.total_supply, self.circulating_supply)

    @classmethod
    def from_api(cls, data):
        data = super(Statistics, cls).from_api(data)
        cycle = data['cycle']
        date = data['date']
        level = data['level']
        timestamp = data['timestamp']
        total_supply = data['totalSupply']
        circulating_supply = data['circulatingSupply']
        total_bootstrapped = data['totalBootstrapped']
        total_commitments = data['totalCommitments']
        total_activated = data['totalActivated']
        total_created = data['totalCreated']
        total_burned = data['totalBurned']
        total_vested = data['totalVested']
        total_frozen = data['totalFrozen']
        quote = data['quote']
        date = data['date']
        if date:
            date = cls.to_datetime(date)

        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        return cls(cycle, date, level, timestamp, total_supply, circulating_supply, total_bootstrapped, total_commitments, total_activated, total_created, total_burned, total_vested, total_frozen, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of end-of-block statistics.

        Keyword Parameters:
            level (int):  Filters statistics by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters statistics by timestamp.  Supports standard modifiers.
            sort (str):  Sorts delegators by specified field. Supported fields: id (default), level, cycle, date. Support sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Example:
            >>> statistics = Statistics.get(level__gt=150000)
        """
        path = 'v1/statistics'
        optional_base_params = ['level', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        quote = kwargs.get('quote')
        if quote:
            params['quote'] = quote
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def daily(cls, **kwargs):
        """
        Returns a list of end-of-day statistics.

        Keyword Parameters:
            date (date|datetime):  Filters statistics by date.  Supports standard modifiers.
            sort (str):  Sorts delegators by specified field. Supported fields: id (default), level, cycle, date.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Example:
            >>> daily_statistics = Statistics.daily()
        """
        path = 'v1/statistics/daily'
        quote = kwargs.pop('quote', None)
        optional_base_params = ['date'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        if quote:
            params['quote'] = quote
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def cyclic(cls, **kwargs):
        """
        Returns a list of end-of-cycle statistics.

        Keyword Parameters:
            cycle (int):  Filters statistics by cycle.  Supports standard modifiers.
            sort (str):  Sorts delegators by specified field. Supported fields: id (default), level, cycle, date.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Example:
            >>> daily_statistics = Statistics.cyclic()
        """
        path = 'v1/statistics/cyclic'
        quote = kwargs.pop('quote', None)
        optional_base_params = ['cycle'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        if quote:
            params['quote'] = quote
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def current(cls, **kwargs):
        """
        Returns statistics at the end of a head block.

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Statistics

        Example:
            >>> current_statistics = Statistics.current()
        """
        path = 'v1/statistics/current'
        params = dict()
        quote = kwargs.pop('quote', None)
        if quote:
            params['quote'] = quote
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return cls.from_api(data)


if __name__ == '__main__':
    import argparse
    from datetime import datetime
    parser = argparse.ArgumentParser(description='Fetch statistics for a given cycle/date')
    parser.add_argument('-d', '--domain', type=str, default=Statistics.domain, help='tzKT domain to fetch data from')
    parser.add_argument('-l', '--limit', type=int, default=10000, help='maximum number of statistics')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--date', type=str, help='date to fetch statistics for (YYYY-MM-DD)')
    group.add_argument('--cycle', type=str, help='cycle to fetch statistics for')

    args = parser.parse_args()
    kwargs = dict(domain=args.domain, limit=args.limit)
    if args.date:
        date = datetime.strptime(args.date, '%Y-%m-d')
        statistics = Statistics.daily(date, **kwargs)
    else:
        kwargs['cycle'] = args.cycle
        statistics = Statistics.cyclic(**kwargs)

    for item in statistics:
        print(item)
