from .base import Base
from . import account

__all__ = ('ShortSoftware', 'Delegate')


class ShortSoftware(Base):
    __slots__ = ('version', 'date')

    def __init__(self, version, date):
        self.version = version
        self.date = date

    @classmethod
    def from_api(cls, data):
        version = data['version']
        date = cls.to_datetime(data['date'])
        return cls(version, date)


class Delegate(account.AccountBase):
    __slots__ = ('type', 'alias', 'address', 'public_key', 'revealed', 'balance', 'frozen_deposits', 'frozen_rewards', 'frozen_fees', 'counter', 'delegate', 'delegation_level', 'delegation_time', 'staking_balance', 'num_contracts', 'num_delegators', 'num_blocks', 'num_endorsements', 'num_ballots', 'num_proposals', 'num_activations', 'num_double_baking', 'num_double_endorsing', 'num_nonce_revelations', 'num_relevation_penalties', 'num_delegations', 'num_originations', 'num_transactions', 'num_reveals', 'num_migrations', 'first_activity', 'first_activity_time', 'last_activity', 'last_activity_time', 'contracts', 'operations', 'metadata', 'software')

    def __init__(self, type, alias, address, publicKey, revealed, balance, frozen_deposits, frozen_rewards, frozen_fees, counter, delegate, delegationLevel, delegationTime, staking_balance, numContracts, num_delegators, num_blocks, num_endorsements, num_ballots, num_proposals, numActivations, num_double_baking, num_double_endorsing, num_nonce_revelations, num_relevation_penalties, numDelegations, numOriginations, numTransactions, numReveals, numMigrations, firstActivity, firstActivityTime, lastActivity, lastActivityTime, contracts, operations, metadata, software):
        super(Delegate, self).__init__(type, alias, address, publicKey, revealed, balance, counter, delegationLevel, delegationTime, numContracts, numActivations, numDelegations, numOriginations, numTransactions, numReveals, numMigrations, firstActivity, firstActivityTime, lastActivity, lastActivityTime, contracts, operations, metadata)
        self.frozen_deposits = frozen_deposits
        self.frozen_rewards = frozen_rewards
        self.frozen_fees = frozen_fees
        self.delegate = delegate
        self.staking_balance = staking_balance
        self.num_delegators = num_delegators
        self.num_blocks = num_blocks
        self.num_ballots = num_ballots
        self.num_endorsements = num_endorsements
        self.num_proposals = num_proposals
        self.num_double_baking = num_double_baking
        self.num_double_endorsing = num_double_endorsing
        self.num_nonce_revelations = num_nonce_revelations
        self.num_relevation_penalties = num_relevation_penalties
        self.software = software

    @classmethod
    def from_api(cls, data):
        data = super(Delegate, cls).from_api(data)
        type = data['type']
        alias = data['alias']
        address = data['address']
        publicKey = data['publicKey']
        revealed = data['revealed']
        balance = data['balance']
        frozen_deposits = data['frozenDeposits']
        frozen_rewards = data['frozenRewards']
        frozen_fees = data['frozenFees']
        counter = data['counter']
        delegate = data['delegate']
        delegationLevel = data['delegationLevel']
        delegationTime = data['delegationTime']
        staking_balance = data['stakingBalance']
        numContracts = data['numContracts']
        num_delegators = data['numDelegators']
        num_blocks = data['numBlocks']
        num_endorsements = data['numEndorsements']
        num_ballots = data['numBallots']
        num_proposals = data['numProposals']
        numActivations = data['numActivations']
        num_double_baking = data['numDoubleBaking']
        num_double_endorsing = data['numDoubleEndorsing']
        num_nonce_revelations = data['numNonceRevelations']
        num_relevation_penalties = data['numRelevationPenalties']
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
        software = data['software']
        if software:
            software = ShortSoftware.from_api(software)
        if firstActivityTime:
            firstActivityTime = cls.to_datetime(firstActivityTime)
        if lastActivityTime:
            lastActivityTime = cls.to_datetime(lastActivityTime)

        return cls(type, alias, address, publicKey, revealed, balance, frozen_deposits, frozen_rewards, frozen_fees, counter, delegate, delegationLevel, delegationTime, staking_balance, numContracts, num_delegators, num_blocks, num_endorsements, num_ballots, num_proposals, numActivations, num_double_baking, num_double_endorsing, num_nonce_revelations, num_relevation_penalties, numDelegations, numOriginations, numTransactions, numReveals, numMigrations, firstActivity, firstActivityTime, lastActivity, lastActivityTime, contracts, operations, metadata, software)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of delegate accounts.

        Keyword Parameters:
            active (bool):  Delegate status to filter by (true - only active, false - only deactivated, undefined - all delegates).
            lastActivity (date|datetime):  Filters delegates by last activity level (where the delegate was updated). Supports standard modifiers.
            sort (str):  Sorts delegators by specified field. Supported fields: id (default), activationLevel, deactivationLevel, stakingBalance, balance, numDelegators.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list:  Delegate accounts meeting the specified criteria

        Example:
            >>> delegates = Delegate.get(active=True)
        """
        path = 'v1/delegates'
        optional_base_params = ['active', 'lastActivity'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def count(cls, **kwargs):
        """
        Returns a number of delegate accounts.

        Keyword Parameters:
            active (bool):  Delegate status to filter by (true - only active, false - only deactivated, undefined - all delegates).
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Example:
            >>> delegate_count = Delegate.count(active=True)
        """
        path = 'v1/delegates/count'
        params = dict()
        if 'active' in kwargs:
            params['active'] = kwargs.pop('active')
        response = cls._request(path, params=params, **kwargs)
        data = response.content
        return int(data)

    @classmethod
    def by_address(cls, address, **kwargs):
        """
        Returns a delegate with the specified address.

        Parameters:
            address (str):  Delegate address (starting with tz)

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Delegate

        Example:
            >>> address = 'tz...'
            >>> delegate = Delegate.by_address(address)
        """
        path = 'v1/delegates/%s' % address
        response = cls._request(path, **kwargs)
        data = response.json()
        return Delegate.from_api(data)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fetch Delegates by address')
    parser.add_argument('-d', '--domain', type=str, default=Delegate.domain, help='tzKT domain to fetch data from')
    parser.add_argument('-a', '--address', type=str, required=True, help='Address of a delegate')

    args = parser.parse_args()
    kwargs = dict(domain=args.domain)
    delegate = Delegate.by_address(address=args.address, **kwargs)
    print(repr(delegate))
