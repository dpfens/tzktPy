from .base import Base
__all__ = ('BigMap', 'BigMapType', 'BigMapKey', 'BigMapUpdate')


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
        """
        Fetches BigMaps based on the specified criteria.

        Keyword Parameters:
            micheline (int): Format of the bigmap key and value type: 0 - JSON, 2 - Micheline.
            contract (str):  Filters bigmaps by smart contract address.  Supports standard modifiers.
            path (str):  Filters bigmaps by path in the contract storage.  Supports standard modifiers.
            tags (list|tuple|set): Filters bigmaps by tags. Support set modifiers.
            lastLevel (int):  Filters bigmaps by the last update level. Support standard modifiers.
            sort (str):  Sorts bigmaps by specified field. Supported fields: id (default), ptr, firstLevel, lastLevel, totalKeys, activeKeys, updates.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list: BigMaps meeting the specified criteria.

        Example:
            >>> bigmaps = BigMap.get(active=True)
        """
        path = 'v1/bigmaps'
        params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['contract', 'path', 'lastLevel', 'tags']
        params, parsed_params = cls.prepare_modifiers(kwargs, include=optional_base_params)
        for param in parsed_params.get('tags', []):
            params[params] = ','.join(params[param])

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
        """
        Fetches a BigMap by the given id.

        Keyword Parameters:
            micheline (int): Format of the bigmap key and value type: 0 - JSON, 2 - Micheline.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            BigMap: BigMap with the given id.

        Example:
            >>> bigmap_id = ''
            >>> bigmap = BigMap.by_id(bigmap_id)
        """
        path = 'v1/bigmaps/%s' % id
        params = dict()
        micheline = kwargs.pop('micheline', None)
        if micheline is not None:
            params['micheline'] = micheline
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def by_contract(cls, address, **kwargs):
        """
        Returns all active bigmaps allocated in the given contract storage.

        Keyword Parameters:
            micheline (int): Format of the bigmap key and value type: 0 - JSON, 2 - Micheline.
            tags (list|tuple|set): Filters bigmaps by tags. Support set modifiers.
            sort (str):  Sorts bigmaps by specified field. Supported fields: id (default), ptr, firstLevel, lastLevel, totalKeys, activeKeys, updates.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list: Active BigMaps allocated to the given contract.

        Example:
            >>> contract_address = 'KT...'
            >>> bigmaps = BigMap.by_contract(contract_address)
        """
        path = 'v1/contracts/%s/bigmaps' % address
        optional_base_params = ['tags'] + list(cls.pagination_parameters)
        params, parsed_params = cls.prepare_modifiers(kwargs, include=optional_base_params)
        for param in parsed_params.get('tags', []):
            params[params] = ','.join(params[param])

        micheline = kwargs.pop('micheline', None)
        if micheline is not None:
            params['micheline'] = micheline
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_name(cls, address, name, **kwargs):
        """
        Returns contract bigmap with the specified name or storage path.

        Parameters:
            address (str):  Address of the given smart contract
            name (str):  Bigmap name is the last piece of the bigmap storage path. For example, if the storage path is ledger or assets.ledger, then the name is ledger. If there are multiple bigmaps with the same name, for example assets.ledger and tokens.ledger, you can specify the full path.

        Keyword Parameters:
            micheline (int): Format of the bigmap key and value type: 0 - JSON, 2 - Micheline.

            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            BigMaps:  The corresponding BigMap.

        Example:
            >>> contract_address = 'KT...'
            >>> bigmaps = BigMap.by_name(contract_address, 'metadata')
        """
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
        """
        Returns a type of the bigmap with the specified Id in Micheline format (with annotations).

        Parameters:
            id (str):  Id of a BigMap

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            BigMapType

        Example:
            >>> bigmap_id = ''
            >>> bigmap = BigMapType.by_id(contract_address, 'metadata')
        """
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
        """
        Returns a list of all bigmap key updates.

        Keyword Parameters:
            bigmap (int):  Filters updates by bigmap ptr. Supports standard modifiers.
            path (str):  Filters updates by bigmap path.  Supports standard modifiers.
            contract (str):  Filters updates by bigmap contract.  Supports standard modifiers.
            action (str):  Filters updates by action.  Supports standard modifiers.
            value(str):  Filters updates by JSON value. Note, this query parameter supports the following format: `?value{__path?}{__mode?}=...`, so you can specify a path to a particular field to filter by, for example: `value__balance__gt=...`.
            level (int):  Filters updates by level.  Supports standard modifiers.
            micheline (int): Format of the bigmap key and value type: 0 - JSON, 2 - Micheline.
            tags (list|tuple|set): Filters bigmaps by tags. Support set modifiers.
            sort (str):  Sorts bigmap updates by specified field. Supported fields: id (default).  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list: BigMapUpdate matching the given criteria


        Example:
            >>> bigmap_updates = BigMapUpdate.get(level__gt=100000)
        """
        path = 'v1/bigmaps/updates'
        optional_base_params = ['bigmap', 'path', 'contract', 'action', 'value', 'level']
        params, param_mappings = cls.prepare_modifiers(kwargs, include=optional_base_params)
        for param in param_mappings.get('tags', []):
            params[param] = ','.join(params[param])

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
        """
        Returns a list of bigmap keys by BigMap id.

        Parameters:
            id (int):  Bigmap Id.

        Keyword Parameters:
            active (bool): Filters keys by status.
            key (str):  Filters keys by JSON key. Note, this query parameter supports the following format: `?key{__path?}{__mode?}=...`, so you can specify a path to a particular field to filter by, for example: `?key__token_id=...`.
            path (str):  Filters updates by bigmap path.  Supports standard modifiers.
            value(str):  Filters updates by JSON value. Note, this query parameter supports the following format: `?value{__path?}{__mode?}=...`, so you can specify a path to a particular field to filter by, for example: `value__balance__gt=...`.
            lastLevel (int):  Filters bigmap keys by the last update level  Supports standard modifiers.
            micheline (int): Format of the bigmap key and value type: 0 - JSON, 2 - Micheline.
            sort (str):  Sorts bigmaps by specified field. Supported fields: id (default), ptr, firstLevel, lastLevel, totalKeys, activeKeys, updates.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list: BigMapKeys matching the given criteria

        Example:
            >>> bigmap_id = 123
            >>> bigmap_keys = BigMapKey.by_bigmap(level__gt=100000)
        """
        path = 'v1/bigmaps/%s/keys' % id
        optional_base_params = ['key', 'value', 'lastLevel']
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_key(cls, id, key, **kwargs):
        """
        Returns a list of bigmap keys by BigMap id.

        Parameters:
            id (int):  Bigmap Id.
            key (str):  Either a key hash (`expr123...`) or a plain value (`abcde...`). Even if the key is complex (an object or an array), you can specify it as is, for example, `/keys/{"address":"tz123","token":123}`.

        Keyword Parameters:
            micheline (int): Format of the bigmap key and value type: 0 - JSON, 2 - Micheline.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list: BigMapKeys matching the given criteria

        Example:
            >>> bigmap_id = 123
            >>> bigmap_keys = BigMapKey.by_bigmap(level__gt=100000)
        """
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
