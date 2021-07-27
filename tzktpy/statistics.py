from .base import Base


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
        path = 'v1/statistics'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['level', 'quote']
        optional_params = cls.get_comparator_fields(kwargs, optional_base_params, cls.comparator_suffixes)

        timestamp_params = cls.get_comparator_fields(kwargs, ['timestamp'], cls.comparator_suffixes)
        params = dict()
        params.update(pagination_params)
        params.update(optional_params)

        for param in timestamp_params:
            value = timestamp_params[param]
            params[param] = value.isoformat()
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def daily(cls, date, **kwargs):
        path = 'v1/statistics/daily'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_params = cls.get_comparator_fields(kwargs, ['quote'], cls.comparator_suffixes)

        timestamp_params = cls.get_comparator_fields(kwargs, ['date'], cls.comparator_suffixes)
        params = dict()
        params.update(pagination_params)
        params.update(optional_params)

        for param in timestamp_params:
            value = timestamp_params[param]
            params[param] = value.isoformat()
        response = cls._request(path, params=params, **kwargs)
        response = cls._request(path)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def cyclic(cls, **kwargs):
        path = 'v1/statistics/cyclic'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_params = cls.get_comparator_fields(kwargs, ['cycle'], cls.comparator_suffixes)

        timestamp_params = cls.get_comparator_fields(kwargs, ['date'], cls.comparator_suffixes)
        params = dict()
        params.update(pagination_params)
        params.update(optional_params)

        for param in timestamp_params:
            value = timestamp_params[param]
            params[param] = value.isoformat()
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def current(cls, **kwargs):
        path = 'v1/statistics/current'
        params = dict()
        quote = kwargs.get('quote')
        if quote:
            params['quote'] = quote
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return cls.from_api(data)


if __name__ == '__main__':
    import argparse
    from datetime import datetime
    parser = argparse.ArgumentParser(description='Fetch statistics')
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
