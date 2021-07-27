from .base import Base


class Operation(Base):

    def __init__(self, type, id, level, timestamp, block, hash, delegate, slots, deposit, rewards, quote):
        self.type = type
        self.id = id
        self.level = level
        self.timestamp = timestamp
        self.block = block
        self.hash = hash
        self.delegate = delegate
        self.slots = slots
        self.deposit = deposit
        self.rewards = rewards
        self.quote = quote

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<%s %s type=%r, id=%r, level=%r, timestamp=%s, hash=%r>' % (self.__class__.__name__, id(self), self.type, self.id, self.level, self.timestamp, self.hash)

    @classmethod
    def from_api(cls, data):
        data = super(Operation, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        block = data['blocks']
        hash = data['hash']
        delegate = data['delegate']
        slots = data['slots']
        deposit = data['deposit']
        rewards = data['rewards']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, hash, delegate, slots, deposit, rewards, quote)

    @classmethod
    def by_hash(cls, hash, **kwargs):
        path = 'v1/operations/%s' % hash
        params = dict()
        quote = kwargs.get('quote')
        if quote:
            params['quote'] = quote

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash_counter(cls, hash, counter, **kwargs):
        path = 'v1/operations/%s/%s' % (hash, counter)

        params = dict()
        micheline = kwargs.pop('micheline', None)
        if micheline:
            params['micheline'] = micheline

        quote = kwargs.get('quote', None)
        if quote:
            params['quote'] = quote
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_account(cls, address, **kwargs):
        path = 'v1/accounts/%s/operations' % address

        valid_parameters = set(['type', 'initiator', 'target', 'prevDelegate', 'newDelegate', 'contractManager', 'contractDelegate', 'originatedContract', 'accuser', 'offender', 'baker', 'level', 'timestamp', 'entrypoint', 'parameter', 'status', 'lastId', 'limit', 'micheline', 'quote'])
        valid_included_parameters = set(kwargs) & valid_parameters

        params = dict((key, kwargs[key]) for key in valid_included_parameters)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def _type_by_hash(cls, type, **kwargs):
        path = 'v1/operations/%s/%s' % (type, hash)
        params = dict()
        quote = kwargs.get('quote')
        if quote:
            params['quote'] = quote
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def _type_count(cls, type, **kwargs):
        params = dict()
        level = kwargs.get('level')
        if level:
            params['level'] = level

        timestamp = kwargs.get('timestamp')
        if timestamp:
            params['timestamp'] = timestamp.isoformat()

        path = 'v1/operations/%s/count' % type
        response = cls._request(path, params=params, **kwargs)
        raw_count = response.content
        return int(raw_count)

    @classmethod
    def get_endorsements(cls, **kwargs):
        path = 'v1/operations/endorsements/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['delegate', 'level']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def endorsements_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('endorsements', hash, **kwargs)

    @classmethod
    def endorsements_count(cls, **kwargs):
        return cls._type_count('endorsements', **kwargs)

    @classmethod
    def get_ballots(cls, **kwargs):
        path = 'v1/operations/ballots/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['delegate', 'level', 'epoch', 'period']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def ballot_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('ballots', hash, **kwargs)

    @classmethod
    def ballots_count(cls, **kwargs):
        return cls._type_count('ballots', **kwargs)

    @classmethod
    def get_proposals(cls, **kwargs):
        path = 'v1/operations/proposals/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['delegate', 'level', 'epoch', 'period']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def proposals_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('proposals', hash, **kwargs)

    @classmethod
    def proposals_count(cls, **kwargs):
        return cls._type_count('proposals', **kwargs)

    @classmethod
    def get_activations(cls, **kwargs):
        path = 'v1/operations/activations/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['account', 'level']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def activations_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('activations', hash, **kwargs)

    @classmethod
    def activations_count(cls, **kwargs):
        return cls._type_count('activations', **kwargs)

    @classmethod
    def get_double_bakings(cls, **kwargs):
        path = 'v1/operations/double_baking/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['accuser', 'offender', 'level']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def double_bakings_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('double_baking', hash, **kwargs)

    @classmethod
    def double_bakings_count(cls, **kwargs):
        return cls._type_count('double_baking', **kwargs)

    @classmethod
    def get_double_endorsings(cls, **kwargs):
        path = 'v1/operations/double_endorsing/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['accuser', 'offender', 'level']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def double_endorsings_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('double_endorsing', hash, **kwargs)

    @classmethod
    def double_endorsings_count(cls, **kwargs):
        return cls._type_count('double_endorsing', **kwargs)

    @classmethod
    def get_nonce_revelations(cls, **kwargs):
        path = 'v1/operations/nonce_revelations/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['baker', 'sender', 'level']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def nonce_revelations_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('nonce_revelations', hash, **kwargs)

    @classmethod
    def nonce_revelations_count(cls, **kwargs):
        return cls._type_count('nonce_revelations', **kwargs)

    @classmethod
    def get_delegations(cls, **kwargs):
        path = 'v1/operations/delegations/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['initiator', 'sender', 'prevDelegate', 'newDelegate', 'level', 'status']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def delegations_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('delegations', hash, **kwargs)

    @classmethod
    def delegations_count(cls, **kwargs):
        return cls._type_count('delegations', **kwargs)

    @classmethod
    def get_originations(cls, **kwargs):
        path = 'v1/operations/originations/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['initiator', 'sender', 'contractManager', 'contractDelegate', 'originatedContract', 'typeHash', 'codeHash', 'level']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def originations_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('originations', hash, **kwargs)

    @classmethod
    def originations_count(cls, **kwargs):
        return cls._type_count('originations', **kwargs)

    @classmethod
    def get_transactions(cls, **kwargs):
        path = 'v1/operations/transactions/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['initiator', 'sender', 'target', 'amount', 'level', 'entrypoint', 'parameter', 'status']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def transactions_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('transactions', hash, **kwargs)

    @classmethod
    def transactions_count(cls, **kwargs):
        return cls._type_count('transactions', **kwargs)

    @classmethod
    def get_reveals(cls, **kwargs):
        path = 'v1/operations/reveals/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['sender', 'level',  'status']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def reveals_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('reveals', hash, **kwargs)

    @classmethod
    def reveals_count(cls, **kwargs):
        return cls._type_count('reveals', **kwargs)

    @classmethod
    def get_migrations(cls, **kwargs):
        path = 'v1/operations/migrations/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['account', 'kind', 'balanceChange', 'level']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def migrations_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('migrations', hash, **kwargs)

    @classmethod
    def migrations_count(cls, **kwargs):
        return cls._type_count('migrations', **kwargs)

    @classmethod
    def get_revelation_penalties(cls, **kwargs):
        path = 'v1/operations/revelation_penalties/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['baker', 'level']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def revelation_penalties_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('revelation_penalties', hash, **kwargs)

    @classmethod
    def revelation_penalties_count(cls, **kwargs):
        return cls._type_count('revelation_penalties', **kwargs)

    @classmethod
    def get_bakings(cls, **kwargs):
        path = 'v1/operations/baking/'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['baker', 'level']
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
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def bakings_by_hash(cls, hash, **kwargs):
        return cls._type_by_hash('baking', hash, **kwargs)

    @classmethod
    def bakings_count(cls, **kwargs):
        return cls._type_count('baking', **kwargs)


if __name__ == '__main__':
    import datetime
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    bakings = Operation.get_bakings(timestamp__gt=yesterday, limit=10000)
    print(bakings)
