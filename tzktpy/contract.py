from .base import Base
from . import account
__all__ = ('EntryPoint', 'Contract')


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
        """
        Returns contract's entrypoint with specified name.

        Parameters:
            address (str):  Contract address (starting with KT)
            name (str):  Entrypoint name

        Keyword Parameters:
            json (bool):  Include parameters schema in human-readable JSON format
            micheline (bool):  Include parameters schema in micheline format
            michelson (bool):  Include parameters schema in michelson format
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            EntryPoint

        Examples:
            >>> address = 'KT1WEHHVMWxQUtkWAgrJBFGXjJ5YqZVgfPVE'
            >>> EntryPoint.by_name(name, 'approve')
        """
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
        metadata = data['metadata']
        if delegationTime:
          delegationTime = cls.to_datetime(delegationTime)

        if firstActivityTime:
          firstActivityTime = cls.to_datetime(firstActivityTime)

        if lastActivityTime:
          lastActivityTime = cls.to_datetime(lastActivityTime)

        return cls(type, alias, address, publicKey, revealed, balance, counter, delegate, delegationLevel, delegationTime, numContracts, numActivations, numDelegations, numOriginations, numTransactions, numReveals, numMigrations, firstActivity, firstActivityTime, lastActivity, lastActivityTime, contracts, operations, metadata)

    @classmethod
    def count(cls, kind, **kwargs):
        """
        Returns a number of contract accounts.

        Parameters:
            kind (str): Contract kind to filter by (delegator_contract or smart_contract).

        Keyword Parameters:
            json (bool):  Include parameters schema in human-readable JSON format
            micheline (bool):  Include parameters schema in micheline format
            michelson (bool):  Include parameters schema in michelson format
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> smart_contract_count = Contract.count('smart_contract')
        """
        path = 'v1/contracts/count'
        params = dict(kind=kind)
        response = cls._request(path, params=params, **kwargs)
        data = response.content
        return int(data)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of contract accounts.

        Keyword Parameters:
            kind (str): Contract kind to filter by (delegator_contract or smart_contract). Supports set modifiers.
            creator (str):  Filters contracts by creator.  Supports standard modifiers.
            manager (str):  Filters contracts by manager.  Supports standard modifiers.
            delegate (str):  Filters contracts by delegate.  Supports standard modifiers.
            lastActivity (date|datetime):  Filters contracts by last activity level (where the contract was updated)  Supports standard modifiers.
            typeHash (int):  Filters contracts by 32-bit hash of contract parameter and storage types (helpful for searching similar contracts).  Supports standard modifiers.
            codeHash (int):  Filters contracts by 32-bit hash of contract code (helpful for searching same contracts).  Supports standard modifiers.
            sort (str):  Sorts contracts by specified field. Supported fields: id (default), balance, firstActivity, lastActivity, numTransactions.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> smart_contracts = Contract.get(kind='smart_contract')
        """
        path = 'v1/contracts'
        optional_base_params = ['kind', 'creator', 'manager', 'delegate', 'lastActivity', 'typeHash', 'codeHash'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_account(cls, address, **kwargs):
        """
        Returns a list of contracts created by (or related to) the specified account.

        Keyword Parameters:
            sort (str):  Sorts contracts by specified field. Supported fields: id (default, desc), balance, creationLevel.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> address = 'tz1WEHHVMWxQUtkWAgrJBFGXjJ5YqZVgfPVE'
            >>> contracts = Contract.by_account(address)
        """
        path = 'v1/accounts/%s/contracts' % address
        params, _ = cls.prepare_modifiers(kwargs, include=cls.pagination_parameters)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_address(cls, address, **kwargs):
        """
        Returns a contract account with the specified address.

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Contract

        Examples:
            >>> address = 'KT...'
            >>> contract = Contract.by_address(address)
        """
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
