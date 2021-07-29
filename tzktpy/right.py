from .base import Base
__all__ = ('Right', )


class Right(Base):
    __slots__ = ('type', 'cycle', 'level', 'timestamp', 'priority', 'slots', 'baker', 'status')

    def __init__(self, type, cycle, level, timestamp, priority, slots, baker, status):
        self.type = type
        self.cycle = cycle
        self.level = level
        self.timestamp = timestamp
        self.priority = priority
        self.slots = slots
        self.baker = baker
        self.status = status

    def __repr__(self):
        return '<%s %s type=%r, cycle=%r, level=%r, timestamp=%r, priority=%r, status=%r>' % (self.__class__.__name__, id(self), self.type, self.cycle, self.level, self.timestamp, self.priority, self.status)

    @classmethod
    def from_api(cls, data):
        data = super(Right, cls).from_api(data)
        type = data['type'],
        cycle = data['cycle'],
        level = data['level'],
        timestamp = data['timestamp'],
        priority = data['priority'],
        slots = data['slots'],
        baker = data['baker'],
        status = data['status']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        return cls(type, cycle, level, timestamp, priority, slots, baker, status)

    @classmethod
    def get(cls, **kwargs):
        optional_params = ['type', 'baker', 'cycle', 'level', 'slots', 'priority', 'status'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_params)
        path = 'v1/rights'
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def count(cls, **kwargs):
        path = 'v1/rights/count'
        optional_params = ['type', 'baker', 'cycle', 'level', 'slots', 'priority', 'status'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_params)
        response = cls._request(path, params=params, **kwargs)
        data = response.content
        return int(data)


if __name__ == '__main__':
    rights_count = Right.count()
    print('Total Rights: %i' % rights_count)
    rights = Right.get()
    print(rights)
