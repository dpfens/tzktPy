from .base import Base


class Cycle(Base):
    __slots__ = ('index', 'first_level', 'start_time', 'last_level', 'end_time', 'snapshot_index', 'snapshot_level', 'random_seed', 'total_bakers', 'total_rolls', 'total_staking', 'total_delegators', 'total_delegated', 'quote')

    def __init__(self, index, first_level, start_time, last_level, end_time, snapshot_index, snapshot_level, random_seed, total_bakers, total_rolls, total_staking, total_delegators, total_delegated, quote):
        self.index = index
        self.first_level = first_level
        self.start_time = start_time
        self.last_level = last_level
        self.end_time = end_time
        self.snapshot_index = snapshot_index
        self.snapshot_level = snapshot_level
        self.random_seed = random_seed
        self.total_bakers = total_bakers
        self.total_rolls = total_rolls
        self.total_staking = total_staking
        self.total_delegators = total_delegators
        self.total_delegated = total_delegated
        self.quote = quote

    def __repr__(self):
        return '<%s %s index=%r, first_level=%r, start_time=%r, last_level=%r, end_time=%r, snapshot_index=%r, snapshot_level=%r>' % (self.__class__.__name__, id(self), self.index, self.first_level, self.start_time, self.last_level, self.end_time, self.snapshot_index, self.snapshot_level)

    @classmethod
    def from_api(cls, data):
        data = super(Cycle, cls).from_api(data)
        index = data['index']
        first_level = data['firstLevel']
        start_time = data['startTime']
        last_level = data['lastLevel']
        end_time = data['endTime']
        snapshot_index = data['snapshotIndex']
        snapshot_level = data['snapshotLevel']
        random_seed = data['randomSeed']
        total_bakers = data['totalBakers']
        total_rolls = data['totalRolls']
        total_staking = data['totalStaking']
        total_delegators = data['totalDelegators']
        total_delegated = data['totalDelegated']
        quote = data['quote']
        if start_time:
            start_time = cls.to_datetime(start_time)
        if end_time:
            end_time = cls.to_datetime(end_time)
        return cls(index, first_level, start_time, last_level, end_time, snapshot_index, snapshot_level, random_seed, total_bakers, total_rolls, total_staking, total_delegators, total_delegated, quote)

    @classmethod
    def get(cls, **kwargs):
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['snapshotIndex']
        optional_params = cls.get_comparator_fields(kwargs, optional_base_params, cls.comparator_suffixes)

        params = dict()
        params.update(pagination_params)
        params.update(optional_params)
        quote = kwargs.pop('quote', None)
        if quote:
            params['quote'] = quote

        path = 'v1/cycles'
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_index(cls, index, **kwargs):
        path = 'v1/cycles/%s' % index
        quote = kwargs.pop('quote', None)
        params = dict()
        if quote:
            params['quote'] = quote
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def count(cls, **kwargs):
        path = 'v1/cycles/count'
        response = cls._request(path, **kwargs)
        value = response.content
        return int(value)


if __name__ == '__main__':
    cycle_count = Cycle.count()
    print('Total Cycles: %i' % cycle_count)
    cycles = Cycle.get()
    for cycle in cycles:
        print(cycle)
