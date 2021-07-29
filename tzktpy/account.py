from .base import Base
__all__ = ('AccountMetadata',' AccountBase', 'Account')

class AccountMetadata:
    __slots__ = ('kind', 'alias', 'address', 'balance', 'delegate', 'creationLevel', 'creationTime')

    def __init__(self, kind, alias, address, balance, delegate, creation_level, creation_time):
        self.kind = kind
        self.alias = alias
        self.address = address
        self.balance = balance
        self.delegate = delegate
        self.creation_level = creation_level
        self.creation_time = creation_time

    @classmethod
    def from_api(cls, data):
        kind = data['kind']
        alias = data['alias']
        address = data['address']
        balance = data['balance']
        delegate = data['delegate']
        creation_level = data['creationLevel']
        creation_time = data['creationTime']
        if creation_time:
            creation_time = cls.to_datetime(creation_time)
        return cls(kind, alias, address, balance, delegate, creation_level, creation_time)


class AccountBase(Base):

    def __init__(self, type, alias, address, public_key, revealed, balance, counter, delegation_level, delegation_time, num_contracts, num_activations, num_delegations, num_originations, num_transactions, num_reveals, num_migrations, first_activity, first_activity_time, last_activity, last_activity_time, contracts, operations, metadata):
        self.type = type
        self.alias = alias
        self.address = address
        self.public_key = public_key
        self.revealed = revealed
        self.balance = balance
        self.counter = counter
        self.delegation_level = delegation_level
        self.delegation_time = delegation_time
        self.num_contracts = num_contracts
        self.num_activations = num_activations
        self.num_delegations = num_delegations
        self.num_originations = num_originations
        self.num_transactions = num_transactions
        self.num_reveals = num_reveals
        self.num_migrations = num_migrations
        self.first_activity = first_activity
        self.first_activity_time = first_activity_time
        self.last_activity = last_activity
        self.last_activity_time = last_activity_time
        self.contracts = contracts
        self.operations = operations
        self.metadata = metadata

    def __str__(self):
        return self.address

    def __repr__(self):
        return '<%s %s address=%r, alias=%r, type=%r, balance=%r, first_activity_time=%s, last_activity_time=%s>' % (self.__class__.__name__, id(self), self.address, self.alias, self.type, self.balance, self.first_activity_time, self.last_activity_time)


class Account(AccountBase):

    def __init__(self, type, alias, address, public_Key, revealed, balance, counter, delegation_level, delegation_time, num_contracts, num_activations, num_delegations, num_originations, num_transactions, num_reveals, num_migrations, first_activity, first_activity_time, last_activity, last_activity_time, contracts, operations, metadata):
        super(Account, self).__init__(type, alias, address, public_Key, revealed, balance, counter, delegation_level, delegation_time, num_contracts, num_activations, num_delegations, num_originations, num_transactions, num_reveals, num_migrations, first_activity, first_activity_time, last_activity, last_activity_time, contracts, operations, metadata)

    @classmethod
    def from_api(cls, data):
        data = super(Account, cls).from_api(data)
        type = data['type']
        alias = data['alias']
        address = data['address']
        public_key = data['publicKey']
        revealed = data['revealed']
        balance = data['balance']
        counter = data['counter']
        delegation_level = data.get('delegationLevel')
        delegation_time = data.get('delegationTime')
        if delegation_time:
            delegation_time = cls.to_datetime(delegation_time)
        num_contracts = data['numContracts']
        num_activations = data['numActivations']
        num_delegations = data['numDelegations']
        num_originations = data['numOriginations']
        num_transactions = data['numTransactions']
        num_reveals = data['numReveals']
        num_migrations = data['numMigrations']
        first_activity = data['firstActivity']
        first_activity_time = data['firstActivityTime']
        if first_activity_time:
            first_activity_time = cls.to_datetime(first_activity_time)
        last_activity = data['lastActivity']
        last_activity_time = data['lastActivityTime']
        if last_activity_time:
            last_activity_time = cls.to_datetime(last_activity_time)
        contracts = data['contracts']
        operations = data['operations']
        metadata = data['metadata']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        return cls(type, alias, address, public_key, revealed, balance, counter, delegation_level, delegation_time, num_contracts, num_activations, num_delegations, num_originations, num_transactions, num_reveals, num_migrations, first_activity, first_activity_time, last_activity, last_activity_time, contracts, operations, metadata)

    @classmethod
    def get(cls, **kwargs):
        path = 'v1/accounts'
        optional_base_params = ['type', 'kind', 'delegate', 'balance', 'staked']
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def count(cls, **kwargs):
        path = 'v1/accounts/count'
        optional_base_params = ['type', 'kind', 'balance', 'staked']
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        response = cls._request(path, params=params)
        data = response.content
        return data

    @classmethod
    def by_address(cls, address, **kwargs):
        path = 'v1/accounts/%s' % address
        metadata = kwargs.pop('metadata', False)
        params = dict(metadata=metadata)
        response = cls._request(path, params=params)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def get_metadata(cls, address, **kwargs):
        path = 'v1/accounts/%s/metadata'
        response = cls._request(path)
        data = response.json()
        return data

    @classmethod
    def suggestions(cls, query, **kwargs):
        path = 'v1/suggest/accounts/%s' % query
        response = cls._request(path)
        return response.json()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fetch accounts by address')
    parser.add_argument('addresses', metavar='N', type=str, nargs='+', help='Accounts of addresses to fetch')

    args = parser.parse_args()
    for address in args.addresses:
        account = Account.by_address(address)
        print(repr(account))
