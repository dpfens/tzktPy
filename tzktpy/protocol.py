from .base import Base
__all__ = ('Operation', )


class Protocol(Base):
    __slots__ = ('code', 'hash', 'first_level', 'last_level', 'constants', 'metadata')

    def __init__(self, code, hash, first_level, last_level, constants, metadata):
        self.code = code
        self.hash = hash
        self.first_level = first_level
        self.last_level = last_level
        self.constants = constants
        self.metadata = metadata

    def __str__(self):
        return self.hash

    def __repr__(self):
        alias = self.metadata.get('alias')
        return '<%s %s code=%r, hash=%r, first_level=%r, last_level=%s, alias=%r>' % (self.__class__.__name__, id(self), self.code, self.hash, self.first_level, self.last_level, alias)

    @classmethod
    def from_api(cls, data):
        data = super(Protocol, cls).from_api(data)
        code = data['code']
        hash = data['hash']
        first_level = data['firstLevel']
        last_level = data['lastLevel']
        constants = data['constants']
        metadata = data['metadata']
        return cls(code, hash, first_level, last_level, constants, metadata)

    @classmethod
    def count(cls, **kwargs):
        path = 'v1/protocols/count'
        response = cls._request(path, **kwargs)
        data = response.content
        return int(data)

    @classmethod
    def get(cls, **kwargs):
        path = 'v1/protocols'
        params, _ = cls.prepare_modifiers(kwargs, include=cls.pagination_parameters)
        response = cls._request(path, params=params)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_code(cls, code, **kwargs):
        path = 'v1/voting/protocols/%s' % code
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def by_hash(cls, hash, **kwargs):
        path = 'v1/voting/protocols/%s' % hash
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def by_cycle(cls, cycle, **kwargs):
        path = 'v1/protocols/cycles/%s' % cycle
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def current(cls, **kwargs):
        path = 'v1/protocols/current'
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def suggestions(cls, query, **kwargs):
        path = 'v1/suggest/protocols/%s' % query
        response = cls._request(path, **kwargs)
        data = response.json()
        return data


if __name__ == '__main__':
    current = Protocol.current()
    print(repr(current))
