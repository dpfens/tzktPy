"""
Operations are actions that are taken by accounts on the Tezos blockchain.

Common operations are:

Activation
    Activate accounts that were recommended allocations of tez tokens for donations to the Tezos Foundation fundraiser.
Delegation
    Account lends tokens to a delegate to increase the delegates rolls.

    Increasing the rolls of a delegate gives the delegate more baking rights.

Endorsement
    Accounts endorse that a block is valid and should be added to the blockchain.

    32 delegates are selected to verify that a block has been baked correctly.  Endorsers receive a reward in tex for their services.
Origination
    Account creates an originate account (smart contract).
Transaction
    Transfers funds between accounts between a sender and a target account.

Voting Operations:

Ballot
    Bakers votes for a proposal during a voting cycle.
Proposal
    Baker submits a new proposal or upvotes an existing proposal.
Double Baking
    An account signs multiple blocks for the same level.
Double Endorsing
    An account endorses multiple blocks for the same level.
Nonce Revelation
    Baker reveals the nonce they committed in their baked blocks.
Reveal
    Reveals the public key associated with an implicit account (tz1 address).
Baking
    Bakers validating new blocks on the Tezos blockchain.
"""

from .base import Base
__all__ = ('Operation', 'Endorsement', 'Ballot', 'Proposal', 'Activation', 'DoubleBaking', 'DoubleEndorsing', 'NonceRevelation', 'Delegation', 'Origination', 'Transaction', 'Reveal', 'Migration', 'RevelationPenalty', 'Baking')


class OperationBase(Base):

    __slots__ = ('type', 'id', 'level', 'timestamp', 'block')

    def __init__(self, type, id, level, timestamp, block):
        self.type = type
        self.id = id
        self.level = level
        self.timestamp = timestamp
        self.block = block

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '<%s %s type=%r, id=%r, level=%r, timestamp=%s, block=%r>' % (self.__class__.__name__, id(self), self.type, self.id, self.level, self.timestamp, self.block)

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a list of operations with the specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            micheline (int):  Format of the parameters, storage and diffs: 0 - JSON, 1 - JSON string, 2 - raw micheline, 3 - raw micheline string
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> hash = 'op6hnMitxyMmdoULXeKq6En2KfC1VDWg9nLwoahTqVhgqNimDLi'
            >>> operations = Operation.by_hash(hash)
        """
        path = 'v1/operations/%s' % hash
        params = dict()
        quote = kwargs.pop('quote', None)
        if quote:
            params['quote'] = quote

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash_counter(cls, hash, counter, **kwargs):
        """
        Returns a list of operations with the specified hash and counter.

        Parameters:
            hash (str):  Operation hash
            counter (int): Operation counter

        Keyword Parameters:
            micheline (int):  Format of the parameters, storage and diffs: 0 - JSON, 1 - JSON string, 2 - raw micheline, 3 - raw micheline string
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> hash = 'op6hnMitxyMmdoULXeKq6En2KfC1VDWg9nLwoahTqVhgqNimDLi'
            >>> counter = 2
            >>> operations = Operation.by_hash_counter(hash, counter)
        """
        path = 'v1/operations/%s/%s' % (hash, counter)

        params = dict()
        micheline = kwargs.pop('micheline', None)
        if micheline:
            params['micheline'] = micheline

        quote = kwargs.pop('quote', None)
        if quote:
            params['quote'] = quote
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_address(cls, address, **kwargs):
        """
        Returns a list of operations related to the specified account. Note: for better flexibility this endpoint accumulates query parameters (filters) of each /operations/{type} endpoint, so a particular filter may affect several operation types containing this filter. For example, if you specify an initiator it will affect all transactions, delegations and originations, because all these types have an initiator field.

        Parameters:
            address (str):  Account address (starting with tz or KT)

        Keyword Parameters:
            type (str):  Comma separated list of operation types to return (endorsement, ballot, proposal, activation, double_baking, double_endorsing, nonce_revelation, delegation, origination, transaction, reveal, migration, revelation_penalty, baking). If not specified then all operation types except endorsement and baking will be returned.
            initiator (str):  Filters transactions, delegations and originations by initiator.  Supports standard modifiers.
            sender (str):  Filters transactions, delegations, originations, reveals and seed nonce revelations by sender.  Supports standard modifiers.
            target (str):  Filters transactions by target.  Supports standard modifiers.
            prevDelegate (str):  Filters delegations by prev delegate.  Supports standard modifiers.
            newDelegate (str):  Filters delegations by new delegate.  Supports standard modifiers.
            contractManager (str):  Filters origination operations by manager.  Supports standard modifiers.
            contractDelegate (str):  Filters origination operations by delegate.  Supports standard modifiers.
            originatedContract (str):  Filters origination operations by originated contract.  Supports standard modifiers.
            accuser (str):  Filters double baking operations by accuser.  Supports standard modifiers.
            offender (str):  Filters double baking operations by offender.  Supports standard modifiers.
            baker (str):  Filters nonce revelation operations by baker.  Supports standard modifiers.
            level (str):  Filters operations by level.  Supports standard modifiers.
            timestamp (str):  Filters operations by timestamp.  Supports standard modifiers.
            entrypoint (str):  Filters transactions by entrypoint called on the target contract.  Supports standard modifiers.
            hasInternals (bool):  Filters transactions by presence of internal operations.
            status (str):  Filters transactions, delegations, originations and reveals by operation status (applied, failed, backtracked, skipped).
            micheline (int):  Format of the parameters, storage and diffs: 0 - JSON, 1 - JSON string, 2 - raw micheline, 3 - raw micheline string
            lastId (int):  Id of the last operation received, which is used as an offset for pagination
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> address = 'tz1WEHHVMWxQUtkWAgrJBFGXjJ5YqZVgfPVE'
            >>> operations = Operation.by_address(address)
        """
        path = 'v1/accounts/%s/operations' % address
        optional_base_params = ['type', 'initiator', 'target', 'prevDelegate', 'newDelegate', 'contractManager', 'contractDelegate', 'originatedContract', 'accuser', 'offender', 'baker', 'level', 'timestamp', 'entrypoint', 'parameter', 'status', 'lastId'] + list(cls.pagination_parameters)
        params, param_mappings = cls.prepare_modifiers(kwargs, include=optional_base_params)
        for param in param_mappings.get('type', []):
            params[param] = ','.join(params[param])

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def _type_by_hash(cls, type, **kwargs):
        path = 'v1/operations/%s/%s' % (type, hash)
        params = dict()
        quote = kwargs.pop('quote', None)
        if quote:
            params['quote'] = quote
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def _type_count(cls, type, **kwargs):
        params = dict()
        optional_base_params = ['level', 'timestamp', 'quote']
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        path = 'v1/operations/%s/count' % type
        response = cls._request(path, params=params, **kwargs)
        raw_count = response.content
        return int(raw_count)


class Operation(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'hash')

    def __init__(self, type, id, level, timestamp, block, hash):
        super(Operation, self).__init__(type, id, level, timestamp, block)
        self.hash = hash

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s, block=%r, hash=%r>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.block, self.hash)

    @classmethod
    def from_api(cls, data):
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        hash = data['hash']
        return cls(type, id, level, timestamp, block, hash)


class Endorsement(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'hash', 'delegate', 'slots', 'deposit', 'rewards', 'quote')

    def __init__(self, type, id, level, timestamp, block, hash, delegate, slots, deposit, rewards, quote):
        super(Endorsement, self).__init__(type, id, level, timestamp, block)
        self.hash = hash
        self.slots = slots
        self.deposit = deposit
        self.rewards = rewards
        self.quote = quote

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s, hash=%r, deposit=%r, rewards=%r>' % (self.__class__.__name__, id(self), self.type, self.id, self.level, self.timestamp, self.hash, self.deposit, self.rewards)

    @classmethod
    def from_api(cls, data):
        data = super(Endorsement, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        hash = data['hash']
        slots = data['slots']
        deposit = data['deposit']
        rewards = data['rewards']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, hash, slots, deposit, rewards, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of endorsement operations.

        Keyword Parameters:
            delegate (str):  Filters endorsements by delegate.  Supports standard modifiers.
            level (str):  Filters operations by level.  Supports standard modifiers.
            timestamp (str):  Filters operations by timestamp.  Supports standard modifiers.
            sort (str):  Sorts endorsements by specified field. Supported fields: id (default), level.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> endorsements = Endorsement.get(level__gt=level)
        """
        path = 'v1/operations/endorsements/'
        optional_base_params = ['delegate', 'level', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns an endorsement operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Endorsement

        Examples:
            >>> hash = 'dadfa...'
            >>> endorsement = Endorsement.by_hash(hash)
        """
        return cls._type_by_hash('endorsements', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of endorsement operations.

        Keyword Parameters:
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = Endorsement.count(level__gt=level)
        """
        return cls._type_count('endorsements', **kwargs)


class Ballot(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'hash', 'period', 'proposal', 'delegate', 'rolls', 'vote', 'quote')

    def __init__(self, type, id, level, timestamp, block, hash, period, proposal, delegate, rolls, vote, quote):
        super(Ballot, self).__init__(type, id, level, timestamp, block)
        self.hash = hash
        self.period = period
        self.proposal = proposal
        self.delegate = delegate
        self.rolls = rolls
        self.vote = vote
        self.quote = quote

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s, hash=%r, period=%r, proposal=%r, vote=%r>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.hash, self.period, self.proposal, self.vote)

    @classmethod
    def from_api(cls, data):
        data = super(Ballot, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        hash = data['hash']
        period = data['period']
        proposal = data['proposal']
        delegate = data['delegate']
        rolls = data['rolls']
        vote = data['vote']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, hash, period, proposal, delegate, rolls, vote, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of ballot operations.

        Keyword Parameters:
            delegate (str):  Filters endorsements by delegate.  Supports standard modifiers.
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp.  Supports standard modifiers.
            epoch (int):  Filters ballots by voting epoch.  Supports standard modifiers.
            period (int):  Filters ballots by voting period.  Supports standard modifiers.
            proposal (str):  Filters ballots by proposal hash.  Supports standard modifiers.
            sort (str):  Sorts endorsements by specified field. Supported fields: id (default), level.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> ballots = Ballot.get(level__gt=level)
        """
        path = 'v1/operations/ballots/'
        optional_base_params = ['delegate', 'level', 'epoch', 'period', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a ballot operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Ballot

        Examples:
            >>> hash = 'dadfa...'
            >>> ballot = Ballot.by_hash(hash)
        """
        return cls._type_by_hash('ballots', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of ballot operations.

        Keyword Parameters:
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = Ballot.count(level__gt=level)
        """
        return cls._type_count('ballots', **kwargs)


class Proposal(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'hash', 'period', 'proposal', 'delegate', 'rolls','duplicated', 'quote')

    def __init__(self, type, id, level, timestamp, block, hash, period, proposal, delegate, rolls,duplicated, quote):
        super(Proposal, self).__init__(type, id, level, timestamp, block)
        self.hash = hash
        self.period = period
        self.proposal = proposal
        self.delegate = delegate
        self.rolls = rolls
        self.duplicated = duplicated
        self.quote = quote

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s, hash=%r, period=%r, proposal=%r>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.hash, self.period, self.proposal)

    @classmethod
    def from_api(cls, data):
        data = super(Proposal, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        hash = data['hash']
        period = data['period']
        proposal = data['proposal']
        delegate = data['delegate']
        rolls = data['rolls']
        duplicated = data['duplicated']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, hash, period, proposal, delegate, rolls, duplicated, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of ballot operations.

        Keyword Parameters:
            delegate (str):  Filters endorsements by delegate.  Supports standard modifiers.
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp.  Supports standard modifiers.
            epoch (int):  Filters ballots by voting epoch.  Supports standard modifiers.
            period (int):  Filters ballots by voting period.  Supports standard modifiers.
            proposal (str):  Filters ballots by proposal hash.  Supports standard modifiers.
            duplicated (bool):  Specify whether to include or exclude duplicates, which didn't actually upvote a proposal.
            sort (str):  Sorts endorsements by specified field. Supported fields: id (default), level.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> proposals = Proposal.get(level__gt=level)
        """
        path = 'v1/operations/proposals/'
        optional_base_params = ['delegate', 'level', 'epoch', 'period', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a proposal operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Proposal

        Examples:
            >>> hash = 'dadfa...'
            >>> proposal = Proposal.by_hash(hash)
        """
        return cls._type_by_hash('proposals', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of proposal operations.

        Keyword Parameters:
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = Proposal.count(level__gt=level)
        """
        return cls._type_count('proposals', **kwargs)


class Activation(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'hash', 'account', 'balance', 'quote')

    def __init__(self, type, id, level, timestamp, block, hash, account, balance, quote):
        super(Activation, self).__init__(type, id, level, timestamp, block)
        self.hash = hash
        self.account = account
        self.balance = balance
        self.quote = quote

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s, hash=%r, account=%r, balance=%r>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.hash, self.account, self.balance)

    @classmethod
    def from_api(cls, data):
        data = super(Activation, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        hash = data['hash']
        account = data['account']
        balance = data['balance']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, hash, account, balance, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of activation operations.

        Keyword Parameters:
            account (str):  Filters operations by account.  Supports standard modifiers.
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp.  Supports standard modifiers.
            sort (str):  Sorts endorsements by specified field. Supported fields: id (default), level.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> activations = Activation.get(level__gt=level)
        """
        path = 'v1/operations/activations/'
        optional_base_params = ['account', 'level', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns an activation operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Proposal

        Examples:
            >>> hash = 'dadfa...'
            >>> activation = Activation.by_hash(hash)
        """
        return cls._type_by_hash('activations', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of proposal operations.

        Keyword Parameters:
            level (int):  Filters proposals by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = Proposal.count(level__gt=level)
        """
        return cls._type_count('activations', **kwargs)


class DoubleBaking(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'hash', 'accused_level', 'accuser', 'accuser_rewards', 'offender', 'offender_lost_deposits', 'offender_lost_rewards', 'offender_lost_fees', 'quote')

    def __init__(self, type, id, level, timestamp, block, hash, accused_level, accuser, accuser_rewards, offender, offender_lost_deposits, offender_lost_rewards, offender_lost_fees, quote):
        super(DoubleBaking, self).__init__(type, id, level, timestamp, block)
        self.hash = hash
        self.accused_level = accused_level
        self.accuser = accuser
        self.accuser_rewards = accuser_rewards
        self.offender = offender
        self.offender_lost_deposits = offender_lost_deposits
        self.offender_lost_rewards = offender_lost_rewards
        self.offender_lost_fees = offender_lost_fees
        self.quote = quote

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s, hash=%r, offender=%r, accuser=%r>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.hash, self.offender, self.accuser)

    @classmethod
    def from_api(cls, data):
        data = super(DoubleBaking, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        hash = data['hash']
        accused_level = data['accusedLevel']
        accuser = data['accuser']
        accuser_rewards = data['accuserRewards']
        offender = data['offender']
        offender_lost_deposits = data['offenderLostDeposits']
        offender_lost_rewards = data['offenderLostRewards']
        offender_lost_fees = data['offenderLostFees']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, hash, accused_level, accuser, accuser_rewards, offender, offender_lost_deposits, offender_lost_rewards, offender_lost_fees, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of double baking operations.

        Keyword Parameters:
            anyof (str):  Filters double baking operations by any of the specified fields. Example: `anyof__accuser__offender=tz1...` will return operations where accuser OR offender is equal to the specified value. This parameter is useful when you need to retrieve all operations associated with a specified account.
            accuser (str):  Filters operations by accuser.  Support standard modifiers.
            offender (str):  Filters operations by offender.  Support standard modifiers.
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp.  Supports standard modifiers.
            sort (str):  Sorts endorsements by specified field. Supported fields: id (default), level.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> double_bakings = DoubleBaking.get(level__gt=level)
        """
        path = 'v1/operations/double_baking/'
        optional_base_params = ['anyof', 'accuser', 'offender', 'level', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a double baking operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            DoubleBaking

        Examples:
            >>> hash = 'dadfa...'
            >>> double_baking = DoubleBaking.by_hash(hash)
        """
        return cls._type_by_hash('double_baking', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of double baking operations.

        Keyword Parameters:
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = DoubleBaking.count(level__gt=level)
        """
        return cls._type_count('double_baking', **kwargs)


class DoubleEndorsing(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'hash', 'accused_level', 'accuser', 'accuser_rewards', 'offender', 'offender_lost_deposits', 'offender_lost_rewards', 'offender_lost_fees', 'quote')

    def __init__(self, type, id, level, timestamp, block, hash, accused_level, accuser, accuser_rewards, offender, offender_lost_deposits, offender_lost_rewards, offender_lost_fees, quote):
        super(DoubleEndorsing, self).__init__(type, id, level, timestamp, block)
        self.hash = hash
        self.accused_level = accused_level
        self.accuser = accuser
        self.accuser_rewards = accuser_rewards
        self.offender = offender
        self.offender_lost_deposits = offender_lost_deposits
        self.offender_lost_rewards = offender_lost_rewards
        self.offender_lost_fees = offender_lost_fees
        self.quote = quote

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s, hash=%r, offender=%r, accuser=%r>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.hash, self.offender, self.accuser)

    @classmethod
    def from_api(cls, data):
        data = super(DoubleEndorsing, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        hash = data['hash']
        accused_level = data['accusedLevel']
        accuser = data['accuser']
        accuser_rewards = data['accuserRewards']
        offender = data['offender']
        offender_lost_deposits = data['offenderLostDeposits']
        offender_lost_rewards = data['offenderLostRewards']
        offender_lost_fees = data['offenderLostFees']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, hash, accused_level, accuser, accuser_rewards, offender, offender_lost_deposits, offender_lost_rewards, offender_lost_fees, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of double endorsing operations.

        Keyword Parameters:
            anyof (str):  Filters operations by any of the specified fields. Example: `anyof__accuser__offender=tz1...` will return operations where accuser OR offender is equal to the specified value. This parameter is useful when you need to retrieve all operations associated with a specified account.
            accuser (str):  Filters operations by accuser.  Support standard modifiers.
            offender (str):  Filters operations by offender.  Support standard modifiers.
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp.  Supports standard modifiers.
            sort (str):  Sorts endorsements by specified field. Supported fields: id (default), level.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> double_endorsings = DoubleEndorsing.get(level__gt=level)
        """
        path = 'v1/operations/double_endorsing/'
        optional_base_params = ['anyof', 'accuser', 'offender', 'level', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a double endorsing operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            DoubleEndorsing

        Examples:
            >>> hash = 'dadfa...'
            >>> double_endorsing = DoubleEndorsing.by_hash(hash)
        """
        return cls._type_by_hash('double_endorsing', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of double endorsing operations.

        Keyword Parameters:
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = DoubleEndorsing.count(level__gt=level)
        """
        return cls._type_count('double_endorsing', **kwargs)


class NonceRevelation(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'hash', 'baker', 'baker_rewards', 'sender', 'revealed_level', 'quote')

    def __init__(self, type, id, level, timestamp, block, hash, baker, baker_rewards, sender, revealed_level, quote):
        super(NonceRevelation, self).__init__(type, id, level, timestamp, block)
        self.hash = hash
        self.baker = baker
        self.baker_rewards = baker_rewards
        self.sender = sender
        self.revealed_level = revealed_level
        self.quote = quote

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s, hash=%r, sender=%r, baker=%r, baker_rewards=%r>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.hash, self.sender, self.baker, self.baker_rewards)

    @classmethod
    def from_api(cls, data):
        data = super(NonceRevelation, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        hash = data['hash']
        baker = data['baker']
        baker_rewards = data['bakerRewards']
        sender = data['sender']
        revealed_level = data['revealedLevel']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, hash, baker, baker_rewards, sender, revealed_level, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of nonce revelation operations.

        Keyword Parameters:
            anyof (str):  Filters operations by any of the specified fields. Example: `anyof__baker__sender=tz1...` will return operations where baker OR sender is equal to the specified value. This parameter is useful when you need to retrieve all operations associated with a specified account.
            baker (str):  Filters operations by baker.  Support standard modifiers.
            sender (str):  Filters operations by sender.  Support standard modifiers.
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp.  Supports standard modifiers.
            sort (str):  Sorts endorsements by specified field. Supported fields: id (default), level.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> nonce_revelations = NonceRevelation.get(level__gt=level)
        """
        path = 'v1/operations/nonce_revelations/'
        optional_base_params = ['anyof', 'baker', 'sender', 'level', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a nonce revelation operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            NonceRevelation

        Examples:
            >>> hash = 'dadfa...'
            >>> nonce_revelation = NonceRevelation.by_hash(hash)
        """
        return cls._type_by_hash('nonce_revelations', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of nonce revelation operations.

        Keyword Parameters:
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = NonceRevelation.count(level__gt=level)
        """
        return cls._type_count('nonce_revelations', **kwargs)


class Delegation(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'hash', 'counter', 'initiator', 'sender', 'nonce', 'gas_limit', 'gas_used', 'storage_limit', 'storage_used', 'baker_fee', 'amount', 'prev_delegate', 'new_delegate', 'status', 'errors', 'quote')

    def __init__(self, type, id, level, timestamp, block, hash, counter, initiator, sender, nonce, gas_limit, gas_used, storage_limit, storage_used, baker_fee, amount, prev_delegate, new_delegate, status, errors, quote):
        super(Delegation, self).__init__(type, id, level, timestamp, block)
        self.hash = hash
        self.counter = counter
        self.initiator = initiator
        self.sender = sender
        self.nonce = nonce
        self.gas_limit = gas_limit
        self.gas_used = gas_used
        self.baker_fee = baker_fee
        self.amount = amount
        self.prev_delegate = prev_delegate
        self.new_delegate = new_delegate
        self.status = status
        self.errors = errors
        self.quote = quote

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s, hash=%r, sender=%r, amount=%r, new_delegate=%r>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.hash, self.sender, self.amount, self.new_delegate)

    @classmethod
    def from_api(cls, data):
        data = super(Delegation, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        hash = data['hash']
        counter = data['counter']
        initiator = data['initiator']
        sender = data['sender']
        nonce = data['nonce']
        gas_limit = data['gasLimit']
        gas_used = data['gasUsed']
        baker_fee = data['bakerFee']
        amount = data['amount']
        prev_delegate = data['prevDelegate']
        new_delegate = data['newDelegate']
        status = data['status']
        errors = data['errors']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, hash, counter, initiator, sender, nonce, gas_limit, gas_used, storage_limit, storage_used, baker_fee, amount, prev_delegate, new_delegate, status, errors, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of delegation operations.

        Keyword Parameters:
            anyof (str):  Filters delegations by any of the specified fields. Example: `anyof__prevDelegate__newDelegate='tz1...'` will return operations where prevDelegate OR newDelegate is equal to the specified value. This parameter is useful when you need to retrieve all delegations associated with a specified account.
            initiator (str):  Filters operations by initiator.  Support standard modifiers.
            sender (str):  Filters operations by sender.  Support standard modifiers.
            prevDelegate (str): Filters operations by prev delegate.  Supports standard modifiers.
            newDelegate (str): Filters operations by new delegate.  Supports standard modifiers.
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp.  Supports standard modifiers.
            status (str):  Filters delegations by operation status (applied, failed, backtracked, skipped).
            sort (str):  Sorts delegations by specified field. Supported fields: id (default), level, gasUsed, bakerFee.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> delegations = Delegation.get(level__gt=level)
        """
        path = 'v1/operations/delegations/'
        optional_base_params = ['anyof', 'initiator', 'sender', 'prevDelegate', 'newDelegate', 'level', 'status', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a delegation operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Delegation

        Examples:
            >>> hash = 'dadfa...'
            >>> delegation = Delegation.by_hash(hash)
        """
        return cls._type_by_hash('delegations', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of delegation operations.

        Keyword Parameters:
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = Delegation.count(level__gt=level)
        """
        return cls._type_count('delegations', **kwargs)


class Origination(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'hash', 'counter', 'initiator', 'sender', 'nonce', 'gas_limit', 'gas_used', 'storage_limit', 'storage_used', 'baker_fee', 'storage_fee', 'allocation_fee', 'contract_balance', 'contract_manager', 'contract_delegate', 'code', 'storage', 'diffs', 'status', 'errors', 'originated_contract', 'quote')

    def __init__(self, type, id, level, timestamp, block, hash, counter, initiator, sender, nonce, gas_limit, gas_used, storage_limit, storage_used, baker_fee, storage_fee, allocation_fee, contract_balance, contract_manager, contract_delegate, code, storage, diffs, status, errors, originated_contract, quote):
        super(Origination, self).__init__(type, id, level, timestamp, block)
        self.hash = hash
        self.counter = counter
        self.initiator = initiator
        self.sender = sender
        self.nonce = nonce
        self.gas_limit = gas_limit
        self.gas_used = gas_used
        self.baker_fee = baker_fee
        self.storage_fee = storage_fee
        self.allocation_fee = allocation_fee
        self.contract_balance = contract_balance
        self.contract_manager = contract_manager
        self.contract_delegate = contract_delegate
        self.code = code
        self.storage = storage
        self.diffs = diffs
        self.status = status
        self.errors = errors
        self.originated_contract = originated_contract
        self.quote = quote

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s, hash=%r, sender=%r, contract_balance=%r, originated_contract=%r>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.hash, self.sender, self.contract_balance, self.originated_contract)

    @classmethod
    def from_api(cls, data):
        data = super(Origination, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        hash = data['hash']
        counter = data['counter']
        initiator = data['initiator']
        sender = data['sender']
        nonce = data['nonce']
        gas_limit = data['gasLimit']
        gas_used = data['gasUsed']
        baker_fee = data['bakerFee']
        storage_fee = data['storageFee']
        allocation_fee = data['allocationFee']
        contract_balance = data['contractBalance']
        contract_manager = data['contractManager']
        contract_delegate = data['contractDelegate']
        code = data['code']
        storage = data['storage']
        diffs = data['diffs']
        status = data['status']
        errors = data['errors']
        originated_contract = data['originatedContract']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, hash, counter, initiator, sender, nonce, gas_limit, gas_used, storage_limit, storage_used, baker_fee, storage_fee, allocation_fee, contract_balance, contract_manager, contract_delegate, code, storage, diffs, status, errors, originated_contract, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of origination operations.

        Keyword Parameters:
            anyof (str):  Filters operations by any of the specified fields. Example: `anyof__sender__initiator='tz1...'` will return operations where sender OR initiator is equal to the specified value. This parameter is useful when you need to retrieve all originations associated with a specified account.
            initiator (str):  Filters operations by initiator.  Support standard modifiers.
            sender (str):  Filters operations by sender.  Support standard modifiers.
            contractManager (str):  Filters origination operations by manager.  Supports standard modifiers.
            contractDelegate (str):  Filters origination operations by delegate.  Supports standard modifiers.
            originatedContract (str):  Filters origination operations by originated contract.  Supports standard modifiers.
            typeHash (int):  Filters origination operations by 32-bit hash of originated contract parameter and storage types (helpful for searching originations of similar contracts).  Supports standard modifiers.
            codeHash (int):  Filters origination operations by 32-bit hash of originated contract code (helpful for searching originations of same contracts).  Supports standard modifiers.
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp.  Supports standard modifiers.
            status (str):  Filters origination operations by operation status (applied, failed, backtracked, skipped).
            sort (str):  Sorts originations by specified field. Supported fields: id (default), level, gasUsed, storageUsed, bakerFee, storageFee, allocationFee, contractBalance.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> originations = Origination.get(level__gt=level)
        """
        path = 'v1/operations/originations/'
        optional_base_params = ['anyof', 'initiator', 'sender', 'contractManager', 'contractDelegate', 'originatedContract', 'typeHash', 'codeHash', 'level', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns an origination operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Origination

        Examples:
            >>> hash = 'dadfa...'
            >>> origination = Origination.by_hash(hash)
        """
        return cls._type_by_hash('originations', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of origination operations.

        Keyword Parameters:
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = Origination.count(level__gt=level)
        """
        return cls._type_count('originations', **kwargs)


class Transaction(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'hash', 'sender', 'target', 'quote', 'nonce', 'gas_limit', 'gas_used', 'storage_limit', 'storage_used', 'baker_fee', 'storage_fee', 'allocation_fee', 'amount', 'parameter', 'storage', 'diffs', 'status', 'has_internals')

    def __init__(self, type, id, level, timestamp, block, hash, sender, target, quote, nonce, gas_limit, gas_used, storage_limit, storage_used, baker_fee, storage_fee, allocation_fee, amount, parameter, storage, diffs, status, has_internals):
        super(Transaction, self).__init__(type, id, level, timestamp, block)
        self.hash = hash
        self.sender = sender
        self.target = target
        self.quote = quote
        self.nonce = nonce
        self.gas_limit = gas_limit
        self.gas_used = gas_used
        self.storage_limit = storage_limit
        self.storage_used = storage_used
        self.baker_fee = baker_fee
        self.storage_fee = storage_fee
        self.allocation_fee = allocation_fee
        self.amount = amount
        self.parameter = parameter
        self.storage = storage
        self.diffs = diffs
        self.status = status
        self.has_internals = has_internals

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s, hash=%r, sender=%r, target=%r, amount=%r>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.hash, self.sender, self.target, self.amount)

    @classmethod
    def from_api(cls, data):
        data = super(Transaction, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        hash = data['hash']
        sender = data['sender']
        target = data['target']
        quote = data['quote']
        nonce = data['nonce']
        gas_limit = data['gasLimit']
        gas_used = data['gasUsed']
        storage_limit = data['storageLimit']
        storage_used = data['storageUsed']
        baker_fee = data['bakerFee']
        storage_fee = data['storageFee']
        allocation_fee = data['allocationFee']
        amount = data['amount']
        parameter = data['parameter']
        storage = data['storage']
        diffs = data['diffs']
        status = data['status']
        has_internals = data['hasInternals']
        return cls(type, id, level, timestamp, block, hash, sender, target, quote, nonce, gas_limit, gas_used, storage_limit, storage_used, baker_fee, storage_fee, allocation_fee, amount, parameter, storage, diffs, status, has_internals)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of transaction operations.

        Keyword Parameters:
            anyof (str):  Filters operations by any of the specified fields. Example: `anyof__sender__target='tz1...'` will return operations where sender OR target is equal to the specified value. This parameter is useful when you need to retrieve all transactions associated with a specified account.
            initiator (str):  Filters operations by initiator.  Support standard modifiers.
            sender (str):  Filters operations by sender.  Support standard modifiers.
            target (str):  Filters operations by target.  Support standard modifiers.
            amount (int):  Filters operations by amount (microtez).  Support standard modifiers.
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp.  Supports standard modifiers.
            entrypoint (str):  Filters transactions by entrypoint called on the target contract.  Supports standard modifiers.
            parameter (str):  Filters transactions by parameter value. Note, this query parameter supports the following format: `?parameter{__path?}{__mode?}=...`, so you can specify a path to a particular field to filter by, for example: `?parameter__token_id=...` or `?parameter__sigs__0__ne=...`.
            hasInternals (bool):  Filters transactions by presence of internal operations.
            status (str):  Filters origination operations by operation status (applied, failed, backtracked, skipped).
            sort (str):  Sorts transactions by specified field. Supported fields: id (default), level, gasUsed, storageUsed, bakerFee, storageFee, allocationFee, amount.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> transactions = Transaction.get(level__gt=level)
        """
        path = 'v1/operations/transactions/'
        optional_base_params = ['anyof', 'initiator', 'sender', 'target', 'amount', 'level', 'entrypoint', 'parameter', 'status', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a transaction operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Transaction

        Examples:
            >>> hash = 'dadfa...'
            >>> transaction = Transaction.by_hash(hash)
        """
        return cls._type_by_hash('transactions', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of transaction operations.

        Keyword Parameters:
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            status (str):  Filters transactions by operation status (applied, failed, backtracked, skipped).
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = Transaction.count(level__gt=level)
        """
        return cls._type_count('transactions', **kwargs)


class Reveal(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'hash', 'sender', 'counter', 'gas_limit', 'gas_used', 'baker_fee', 'status', 'errors', 'quote')

    def __init__(self, type, id, level, timestamp, block, hash, sender, counter, gas_limit, gas_used, baker_fee, status, errors, quote):
        super(Reveal, self).__init__(type, id, level, timestamp, block)
        self.hash = hash
        self.sender = sender
        self.counter = counter
        self.gas_limit = gas_limit
        self.gas_used = gas_used
        self.baker_fee = baker_fee
        self.status = status
        self.errors = errors
        self.quote = quote

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s, hash=%r, sender=%r, gas_used=%r>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.hash, self.sender, self.gas_used)

    @classmethod
    def from_api(cls, data):
        data = super(Reveal, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        hash = data['hash']
        sender = data['sender']
        counter = data['counter']
        gas_limit = data['gasLimit']
        gas_used = data['gasUsed']
        baker_fee = data['bakerFee']
        status = data['status']
        errors = data['errors']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, hash, sender, counter, gas_limit, gas_used, baker_fee, status, errors, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of reveal operations.

        Keyword Parameters:
            sender (str):  Filters operations by sender.  Support standard modifiers.
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp.  Supports standard modifiers.
            status (str):  Filters origination operations by operation status (applied, failed, backtracked, skipped).
            sort (str):  Sorts reveals by specified field. Supported fields: id (default), level, gasUsed, bakerFee.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> reveals =  Reveal.get(level__gt=level)
        """
        path = 'v1/operations/reveals/'
        optional_base_params = ['sender', 'level',  'status', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a reveal operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Reveal

        Examples:
            >>> hash = 'dadfa...'
            >>> reveal = Reveal.by_hash(hash)
        """
        return cls._type_by_hash('reveals', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of reveal operations.

        Keyword Parameters:
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = Reveal.count(level__gt=level)
        """
        return cls._type_count('reveals', **kwargs)


class Migration(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'kind', 'account', 'balance_change', 'quote')

    def __init__(self, type, id, level, timestamp, block, kind, account, balance_change, quote):
        super(Migration, self).__init__(type, id, level, timestamp, block)
        self.kind = kind
        self.account = account
        self.balance_change = balance_change
        self.quote = quote

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s, kind=%r, account=%r, balance_change=%r,>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.kind, self.account, self.balance_change)

    @classmethod
    def from_api(cls, data):
        data = super(Migration, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        kind = data['kind']
        account = data['account']
        balance_change = data['balanceChange']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, kind, account, balance_change, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of migration operations.

        Keyword Parameters:
            account (str):  Filters operations by account.  Supports standard modifiers.
            kind (str):  Filters migration operations by kind (bootstrap, activate_delegate, airdrop, proposal_invoice).  Support standard modifiers.
            balanceChange (int):  Filters migration operations by amount.  Supports standard modifiers.
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp.  Supports standard modifiers.
            status (str):  Filters origination operations by operation status (applied, failed, backtracked, skipped).
            sort (str):  Sorts migrations by specified field. Supported fields: id (default), level.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> migrations = Migration.get(level__gt=level)
        """
        path = 'v1/operations/migrations/'
        optional_base_params = ['account', 'kind', 'balanceChange', 'level', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a migration operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Migration

        Examples:
            >>> hash = 'dadfa...'
            >>> migration = Migration.by_hash(hash)
        """
        return cls._type_by_hash('migrations', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of migration operations.

        Keyword Parameters:
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = Migration.count(level__gt=level)
        """
        return cls._type_count('migrations', **kwargs)


class RevelationPenalty(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'baker', 'missed_level', 'lost_reward', 'lost_fees', 'quote')

    def __init__(self, type, id, level, timestamp, block, baker, missed_level, lost_reward, lost_fees, quote):
        super(RevelationPenalty, self).__init__(type, id, level, timestamp, block)
        self.baker = baker
        self.missed_level = missed_level
        self.lost_reward = lost_reward
        self.lost_fees = lost_fees
        self.quote = quote

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s baker=%r, missed_level=%r, lost_reward=%s>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.baker, self.missed_level, self.lost_reward)

    @classmethod
    def from_api(cls, data):
        data = super(RevelationPenalty, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        baker = data['baker']
        missed_level = data['missedLevel']
        lost_reward = data['lostReward']
        lost_fees = data['lostFees']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, baker, missed_level, lost_reward, lost_fees, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of revelation penalty operations.

        Keyword Parameters:
            baker (str):  Filters operations by baker.  Supports standard modifiers.
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp.  Supports standard modifiers.
            status (str):  Filters origination operations by operation status (applied, failed, backtracked, skipped).
            sort (str):  Sorts migrations by specified field. Supported fields: id (default), level.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> revelation_penalties = RevelationPenalty.get(level__gt=level)
        """
        path = 'v1/operations/revelation_penalties/'
        optional_base_params = ['baker', 'level', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a revelation penalty operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            RevelationPenalty

        Examples:
            >>> hash = 'dadfa...'
            >>> revelation_penalty = RevelationPenalty.by_hash(hash)
        """
        return cls._type_by_hash('revelation_penalties', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of revelation penalty operations.

        Keyword Parameters:
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = RevelationPenalty.count(level__gt=level)
        """
        return cls._type_count('revelation_penalties', **kwargs)


class Baking(OperationBase):
    __slots__ = ('type', 'id', 'level', 'timestamp', 'block', 'baker', 'priority', 'deposit', 'reward', 'fees', 'quote')

    def __init__(self, type, id, level, timestamp, block, baker, priority, deposit, reward, fees, quote):
        super(Baking, self).__init__(type, id, level, timestamp, block)
        self.baker = baker
        self.priority = priority
        self.deposit = deposit
        self.reward = reward
        self.fees = fees
        self.quote = quote

    def __repr__(self):
        return '<%s %s id=%r, level=%r, timestamp=%s baker=%r, priority=%r, reward=%r, fees=%r>' % (self.__class__.__name__, id(self), self.id, self.level, self.timestamp, self.baker, self.priority, self.reward, self.fees)

    @classmethod
    def from_api(cls, data):
        data = super(Baking, cls).from_api(data)
        type = data['type']
        id = data['id']
        level = data['level']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        block = data['block']
        baker = data['baker']
        priority = data['priority']
        deposit = data['deposit']
        reward = data['reward']
        fees = data['fees']
        quote = data['quote']
        return cls(type, id, level, timestamp, block, baker, priority, deposit, reward, fees, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of baking operations.

        Keyword Parameters:
            baker (str):  Filters operations by baker.  Supports standard modifiers.
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp.  Supports standard modifiers.
            status (str):  Filters origination operations by operation status (applied, failed, backtracked, skipped).
            sort (str):  Sorts baking operations by specified field. Supported fields: id (default), level.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list

        Examples:
            >>> level = 100000
            >>> bakings = Baking.get(level__gt=level)
        """
        path = 'v1/operations/baking/'
        optional_base_params = ['baker', 'level', 'timestamp'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a baking operation with specified hash.

        Parameters:
            hash (str):  Operation hash

        Keyword Parameters:
            quote (list|tuple|set):  list of ticker symbols to inject historical prices into response
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Baking

        Examples:
            >>> hash = 'dadfa...'
            >>> baking = Baking.by_hash(hash)
        """
        return cls._type_by_hash('baking', hash, **kwargs)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of baking operations.

        Keyword Parameters:
            level (int):  Filters operations by level.  Supports standard modifiers.
            timestamp (date|datetime):  Filters operations by timestamp. Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Examples:
            >>> level = 100000
            >>> count = Baking.count(level__gt=level)
        """
        return cls._type_count('baking', **kwargs)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Fetch Operations performed by/on a Tezos account address')
    parser.add_argument('-a', '--address', type=str, required=True, help='Address of account to report on')
    parser.add_argument('-l', '--limit', type=int, default=1000, help='Maximum number of operations to return')
    parser.add_argument('--domain', type=str, default=Operation.domain, help='tzKT domain to fetch data from')

    args = parser.parse_args()
    kwargs = dict(anyof__sender__target=args.address, offset__pg=0, domain=args.domain, limit=args.limit)
    # page through all pages of operations
    operations = []
    transactions_page = Transaction.get(**kwargs)
    operations += transactions_page
    while transactions_page:
        kwargs['offset__pg'] += 1
        transactions_page = Transaction.get(**kwargs)
        operations += transactions_page

    operations = sorted(operations, key=lambda x: x.timestamp)
    for operation in operations:
        print('%r' % operation)
