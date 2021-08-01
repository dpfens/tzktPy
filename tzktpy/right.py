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
        """
        Returns a list of rights.

        Keyword Parameters:
            type (str):  Filters rights by type (baking, endorsing). Supports standard modifiers.
            baker (str):  Filters rights by baker. Supports standard modifiers.
            cycle (int):  Filters rights by cycle.  Supports standard modifiers.
            level (int):  Filters rights by level.  Supports standard modifiers.
            slots (int):  Filters rights by slots.  Supports standard modifiers.
            priority (int):  Filters rights by priority.  Supports standard modifiers.
            status (str):  Filters rights by status (future, realized, uncovered, missed).
            sort (str):  Sorts rights by specified field. Supported fields: level (default). Support sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Example:
            >>> baking_rights = Right.get(type='baking')
        """
        optional_params = ['type', 'baker', 'cycle', 'level', 'slots', 'priority', 'status'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_params)
        path = 'v1/rights'
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of stored rights.

        Keyword Parameters:
            type (str):  Filters rights by type (baking, endorsing). Supports standard modifiers.
            baker (str):  Filters rights by baker. Supports standard modifiers.
            cycle (int):  Filters rights by cycle.  Supports standard modifiers.
            level (int):  Filters rights by level.  Supports standard modifiers.
            slots (int):  Filters rights by slots.  Supports standard modifiers.
            priority (int):  Filters rights by priority.  Supports standard modifiers.
            status (str):  Filters rights by status (future, realized, uncovered, missed).
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Example:
            >>> baking_rights_count = Right.count(type='baking')
        """
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
