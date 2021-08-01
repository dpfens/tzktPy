from .base import Base
__all__ = ('Protocol', )


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
        """
        Returns the total number of protocols.

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Example:
            >>> protocol_count = Protocol.count()
        """
        path = 'v1/protocols/count'
        response = cls._request(path, **kwargs)
        data = response.content
        return int(data)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of protocols.

        Keyword Parameters:
            sort (str):  Sorts protocols by specified field. Supported fields: id (default), code, firstLevel, lastLevel.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Example:
            >>> protocols = Protocol.get()
        """
        path = 'v1/protocols'
        params, _ = cls.prepare_modifiers(kwargs, include=cls.pagination_parameters)
        response = cls._request(path, params=params)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_code(cls, code, **kwargs):
        """
        Returns a protocol with the specified proto code.

        Parameters:
            code (int):  Protocol code (e.g. 4 for Athens, 5 for Babylon, etc)

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Protocol

        Example:
            >>> athens_protocol = Protocol.by_code(4)
        """
        path = 'v1/voting/protocols/%s' % code
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a protocol with the specified hash.

        Parameters:
            hash (int):  Protocol hash

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Protocol

        Example:
            >>> hash = 'dfsdfsfs...'
            >>> protocol = Protocol.by_hash(hash)
        """
        path = 'v1/voting/protocols/%s' % hash
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def by_cycle(cls, cycle, **kwargs):
        """
        Returns a protocol at the specified cycle.

        Parameters:
            cycle (int):  Cycle index

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Protocol

        Example:
            >>> cycle = 12
            >>> protocol = Protocol.by_cycle(cycle)
        """
        path = 'v1/protocols/cycles/%s' % cycle
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def current(cls, **kwargs):
        """
        Returns current protocol.

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Protocol

        Example:
            >>> protocol = Protocol.current()
        """
        path = 'v1/protocols/current'
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def suggestions(cls, query, **kwargs):
        """
        Returns suggestions for protocols based on a query.

        Parameters:
            query (str):  The query used to generate suggestions

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list: protocol suggestions

        Example:
            >>> protocol = Protocol.suggestions('Granada')
        """
        path = 'v1/suggest/protocols/%s' % query
        response = cls._request(path, **kwargs)
        data = response.json()
        return data


if __name__ == '__main__':
    current = Protocol.current()
    print(repr(current))
