from .base import Base
from . import account


class EntryPoint(Base):
    __slots__ = ('name', 'json_parameters', 'micheline_parameters', 'michelson_parameters', 'unused')

    def __init__(self, name, json_parameters, micheline_parameters, michelson_parameters, unused):
        self.name = name
        self.json_parameters = json_parameters
        self.micheline_parameters = micheline_parameters
        self.michelson_parameters = michelson_parameters
        self.unused = unused

    def __str__(self):
        return self.name

    @classmethod
    def from_api(cls, data):
        name = data['name']
        json_parameters = data['jsonParameters']
        micheline_parameters = data['michelineParameters']
        michelson_parameters = data['michelsonParameters']
        unused = data['unused']
        return cls(name, json_parameters, micheline_parameters, michelson_parameters, unused)

    @classmethod
    def by_name(cls, address, name, **kwargs):
        path = 'v1/contracts/%s/entrypoints/%s' % (address, name)
        params = dict()
        optional_params = ('json', 'micheline', 'michelson')
        for param in optional_params:
            if param in kwargs:
                params[param] = kwargs.pop(param)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return cls.from_api(data)


class Contract(account.AccountBase):
    def __init__(self, type, alias, address, publicKey, revealed, balance, counter, delegate, delegationLevel, delegationTime, numContracts, numActivations, numDelegations, numOriginations, numTransactions , numReveals, numMigrations, firstActivity, firstActivityTime, lastActivity, lastActivityTime, contracts, operations, metadata):
        super(Contract, self).__init__(type, alias, address, publicKey, revealed, balance, counter, delegationLevel, delegationTime, numContracts, numActivations, numDelegations, numOriginations, numTransactions, numReveals, numMigrations, firstActivity, firstActivityTime, lastActivity, lastActivityTime, contracts, operations, metadata)
        self.delegate = delegate

    @classmethod
    def from_api(cls, data):
        type = data['type']
        alias = data['alias']
        address = data['address']
        publicKey = data['publicKey']
        revealed = data['revealed']
        balance = data['balance']
        counter = data['counter']
        delegate = data['delegate']
        delegationLevel = data['delegationLevel']
        delegationTime = data['delegationTime']
        numContracts = data['numContracts']
        numActivations = data['numActivations']
        numDelegations = data['numDelegations']
        numOriginations = data['numOriginations']
        numTransactions = data['numTransactions']
        numReveals = data['numReveals']
        numMigrations = data['numMigrations']
        firstActivity = data['firstActivity']
        firstActivityTime = data['firstActivityTime']
        lastActivity = data['lastActivity']
        lastActivityTime = data['lastActivityTime']
        contracts = data['contracts']
        operations = data['operations']
        metadata: AccountMetadata = data['metadata']
        if delegationTime:
          delegationTime = cls.to_datetime(delegationTime)

        if firstActivityTime:
          firstActivityTime = cls.to_datetime(firstActivityTime)

        if lastActivityTime:
          lastActivityTime = cls.to_datetime(lastActivityTime)

        return cls(type, alias, address, publicKey, revealed, balance, counter, delegate, delegationLevel, delegationTime, numContracts, numActivations, numDelegations, numOriginations, numTransactions, numReveals, numMigrations, firstActivity, firstActivityTime, lastActivity, lastActivityTime, contracts, operations, metadata)

    @classmethod
    def count(cls, kind, **kwargs):
        path = 'v1/contracts/count'
        params = dict(kind=kind)
        response = cls._request(path, params=params, **kwargs)
        data = response.content
        return int(data)

    @classmethod
    def get(cls, **kwargs):
        path = 'v1/contracts'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['kind', 'creator', 'manager', 'delegate', 'lastActivity', 'typeHash', 'codeHash']
        optional_params = cls.get_comparator_fields(kwargs, optional_base_params, cls.comparator_suffixes)

        params = dict()
        params.update(pagination_params)
        params.update(optional_params)

        include_storage = kwargs.pop('includeStorage', False)
        if include_storage:
            params['includeStorage'] = include_storage

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_account(cls, address, **kwargs):
        path = 'v1/accounts/%s/contracts' % address
        params = cls.get_pagination_parameters(kwargs)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_address(cls, address, **kwargs):
        path = 'v1/contracts/%s' % address
        response = cls._request(path, **kwargs)
        data = response.json()
        return Contract.from_api(data)

    @classmethod
    def similar(cls, address, **kwargs):
        path = 'v1/contracts/%s/similar' % address
        params = cls.get_pagination_parameters(kwargs)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def code(cls, address, format, **kwargs):
        path = 'v1/contracts/%s/code' % address
        params = dict(format=format)
        response = cls._request(path, params=params, **kwargs)
        return response.content
