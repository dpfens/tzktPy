from .base import Base


class BigMap(Base):
    __slots__ = ('ptr', 'contract', 'path', 'tags', 'active', 'first_level', 'last_level', 'total_keys', 'active_keys', 'updates', 'key_type', 'value_type')

    def __init__(self, ptr, contract, path, tags, active, first_level, last_level, total_keys, active_keys, updates, key_type, value_type):
        self.ptr = ptr
        self.contract = contract
        self.path = path
        self.tags = tags
        self.active = active
        self.first_level = first_level
        self.last_level = last_level
        self.total_keys = total_keys
        self.active_keys = active_keys
        self.updates = updates
        self.key_type = key_type
        self.value_type = value_type

    def __str__(self):
        return str(self.ptr)

    def __repr__(self):
        return '<%s %s ptr=%r, contract=%r, path=%r, tags=%r, active=%r, first_level=%r, last_level=%r>' % (self.__class__.__name__, id(self), self.ptr, self.contract, self.path, self.tags, self.active, self.first_level, self.last_level)

    @classmethod
    def from_api(cls, data):
        data = super(BigMap, cls).from_api(data)
        ptr = data['ptr']
        contract = data['contract']
        path = data['path']
        tags = data['tags']
        active = data['active']
        first_level = data['firstLevel']
        last_level = data['lastLevel']
        total_keys = data['totalKeys']
        active_keys = data['activeKeys']
        updates = data['updates']
        key_type = data['keyType']
        value_type = data['valueType']
        return cls(ptr, contract, path, tags, active, first_level, last_level, total_keys, active_keys, updates, key_type, value_type)

    @classmethod
    def get(cls, **kwargs):
        path = 'v1/bigmaps'
        params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['contract', 'path', 'lastLevel']
        optional_params = cls.get_comparator_fields(kwargs, optional_base_params, cls.comparator_suffixes)
        optional_tag_params = cls.get_multicomparator_fields(kwargs, ['tags'], cls.set_suffixes)

        params.update(optional_params)
        params.update(optional_tag_params)
        if 'active' in params:
            params['active'] = kwargs.pop('active', None)

        micheline = kwargs.pop('micheline', None)
        if micheline is not None:
            params['micheline'] = micheline

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_id(cls, id, **kwargs):
        path = 'v1/bigmaps/%s' % id
        params = dict()
        micheline = kwargs.pop('micheline', None)
        if micheline is not None:
            params['micheline'] = micheline
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return BigMap.from_api(data)

    @classmethod
    def by_contract(cls, address, **kwargs):
        path = 'v1/contracts/%s/bigmaps' % address
        params = cls.get_pagination_parameters(kwargs)
        optional_tag_params = cls.get_multicomparator_fields(kwargs, ['tags'], cls.set_suffixes)

        params.update(optional_tag_params)
        micheline = kwargs.pop('micheline', None)
        if micheline is not None:
            params['micheline'] = micheline
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_name(address, name, **kwargs):
        path = 'v1/contracts/%s/bigmaps/%s' % (address, name)
        params = dict()
        micheline = kwargs.pop('micheline', None)
        if micheline is not None:
            params['micheline'] = micheline
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return cls.from_api(data)


class BigMapType(Base):
    __slots__ = ('prim', 'args', 'annots')

    def __init__(self, prim, args, annots):
        self.prim = prim
        self.args = args
        self.annots = annots

    @classmethod
    def from_api(cls, data):
        data = super(BigMapType, cls).from_api(data)
        prim = data['prim']
        args = data['args']
        annots = data['annots']
        return cls(prim, args, annots)

    @classmethod
    def get(cls, id, **kwargs):
        path = 'v1/bigmaps/%s/type' % id
        response = cls._request(path, **kwargs)
        data = response.json()
        return BigMapType.from_api(data)


class BigMapUpdate(Base):
    __slots__ = ('id', 'level', 'timestamp', 'bigmap', 'contract', 'path', 'action', 'content')

    def __init__(self, id, level, timestamp, bigmap, contract, path, action, content):
        self.id = id
        self.level = level
        self.timestamp = timestamp
        self.bigmap = bigmap
        self.contract = contract
        self.path = path
        self.action = action
        self.content = content

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%r, contract=%r>' % (self.__class__.__name__, self.id, self.level, self.timestamp, self.contract)

    @classmethod
    def from_api(cls, data):
        data = super(BigMapUpdate, cls).from_api(data)
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        bigmap = data['bigmap']
        contract = data['contract']
        path = data['path']
        action = data['action']
        content = data['content']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        return cls(id, level, timestamp, bigmap, contract, path, action, content)

    @classmethod
    def get(cls, **kwargs):
        path = 'v1/bigmaps/updates'
        params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['bigmap', 'path', 'contract', 'action', 'value', 'level']
        optional_params = cls.get_comparator_fields(kwargs, optional_base_params, cls.comparator_suffixes)
        optional_tag_params = cls.get_multicomparator_fields(kwargs, ['tags'], cls.set_suffixes)

        params.update(optional_params)
        params.update(optional_tag_params)
        micheline = kwargs.pop('micheline', None)
        if micheline is not None:
            params['micheline'] = micheline
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]


class BigMapKey(Base):
    __slots__ = ('id', 'active', 'hash', 'key', 'value', 'first_level', 'last_level', 'updates')

    def __init__(self, id, active, hash, key, value, first_level, last_level, updates):
        self.id = id
        self.active = active
        self.hash = hash
        self.key = key
        self.value = value
        self.first_level = first_level
        self.last_level = last_level
        self.updates = updates

    @classmethod
    def from_api(cls, data):
        id = data['id']
        active = data['active']
        hash = data['hash']
        key = data['key']
        value = data['value']
        first_level = data['firstLevel']
        last_level = data['lastLevel']
        updates = data['updates']
        return cls(id, active, hash, key, value, first_level, last_level, updates)

    @classmethod
    def by_bigmap(cls, id, **kwargs):
        path = 'v1/bigmaps/%s/keys' % id
        params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['key', 'value', 'lastLevel']
        optional_params = cls.get_comparator_fields(kwargs, optional_base_params, cls.comparator_suffixes)

        params.update(optional_params)
        if 'active' in kwargs:
            params['active'] = kwargs.pop('active', None)
        micheline = kwargs.pop('micheline', None)
        if micheline is not None:
            params['micheline'] = micheline
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_key(cls, id, key, **kwargs):
        path = 'v1/bigmaps/%s/keys/%s' % (id, key)
        params = dict()
        micheline = kwargs.pop('micheline', None)
        if micheline is not None:
            params['micheline'] = micheline
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return cls.from_api(data)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fetch bigmaps by contract address')
    parser.add_argument('-d', '--domain', type=str, default=BigMap.domain, help='tzKT domain to fetch data from')
    parser.add_argument('-a', '--address', type=str, help='Address of the contract')

    args = parser.parse_args()
    bigmaps = BigMap.by_contract(args.address, domain=args.domain)
    if bigmaps:
        for bigmap in bigmaps:
            print('%r' % bigmap)
    else:
        print('No bigmaps for the provided address')
