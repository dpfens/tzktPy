from .base import Base


class Reward(Base):
    __slots__ = ('cycle', 'staking_balance', 'delegated_balance', 'num_delegators', 'expected_blocks', 'expected_endorsements', 'future_blocks', 'future_block_rewards', 'future_block_deposits', 'own_blocks', 'own_block_rewards', 'extra_blocks', 'extra_block_rewards', 'missed_own_blocks', 'missed_own_block_rewards', 'missed_extra_blocks', 'missed_extra_block_rewards', 'uncovered_own_blocks', 'uncovered_own_block_rewards', 'uncovered_extra_blocks', 'uncovered_extra_block_rewards', 'block_deposits', 'future_endorsements', 'future_endorsement_rewards', 'future_endorsement_deposits', 'endorsements', 'endorsement_rewards', 'missed_endorsements', 'missed_endorsement_rewards', 'uncovered_endorsements', 'uncovered_endorsement_rewards', 'endorsement_deposits', 'own_block_fees', 'extra_block_fees', 'missed_own_block_fees', 'missed_extra_block_fees', 'uncovered_own_block_fees', 'uncovered_extra_block_fees', 'double_baking_rewards', 'double_baking_lost_deposits', 'double_baking_lost_rewards', 'double_baking_lost_fees', 'double_endorsing_rewards', 'double_endorsing_lost_deposits', 'double_endorsing_lost_fees', 'revelation_rewards', 'revelation_lost_fees', 'quote')

    def __init__(self, cycle, staking_balance, delegated_balance, num_delegators, expected_blocks, expected_endorsements, future_blocks, future_block_rewards, future_block_deposits, own_blocks, own_block_rewards, extra_blocks, extra_block_rewards, missed_own_blocks, missed_own_block_rewards, missed_extra_blocks, missed_extra_block_rewards, uncovered_own_blocks, uncovered_own_block_rewards, uncovered_extra_blocks, uncovered_extra_block_rewards, block_deposits, future_endorsements, future_endorsement_rewards, future_endorsement_deposits, endorsements, endorsement_rewards, missed_endorsements, missed_endorsement_rewards, uncovered_endorsements, uncovered_endorsement_rewards, endorsement_deposits, own_block_fees, extra_block_fees, missed_own_block_fees, missed_extra_block_fees, uncovered_own_block_fees, uncovered_extra_block_fees, double_baking_rewards, double_baking_lost_deposits, double_baking_lost_rewards, double_baking_lost_fees, double_endorsing_rewards, double_endorsing_lost_deposits, double_endorsing_lost_fees, revelation_rewards, revelation_lost_fees, quote):
        self.cycle = cycle
        self.staking_balance = staking_balance
        self.delegated_balance = delegated_balance
        self.num_delegators = num_delegators
        self.expected_blocks = expected_blocks
        self.expected_endorsements = expected_endorsements
        self.future_blocks = future_blocks
        self.future_block_rewards = future_block_rewards
        self.future_block_deposits = future_block_deposits
        self.own_blocks = own_blocks
        self.own_block_rewards = own_block_rewards
        self.extra_blocks = extra_blocks
        self.extra_block_rewards = extra_block_rewards
        self.missed_own_blocks = missed_own_blocks
        self.missed_own_block_rewards = missed_own_block_rewards
        self.missed_extra_blocks = missed_extra_blocks
        self.missed_extra_block_rewards = missed_extra_block_rewards
        self.uncovered_own_blocks = uncovered_own_blocks
        self.uncovered_own_block_rewards = uncovered_own_block_rewards
        self.uncovered_extra_blocks = uncovered_extra_blocks
        self.uncovered_extra_block_rewards = uncovered_extra_block_rewards
        self.block_deposits = block_deposits
        self.future_endorsements = future_endorsements
        self.future_endorsement_rewards = future_endorsement_rewards
        self.future_endorsement_deposits = future_endorsement_deposits
        self.endorsements = endorsements
        self.endorsement_rewards = endorsement_rewards
        self.missed_endorsements = missed_endorsements
        self.missed_endorsement_rewards = missed_endorsement_rewards
        self.uncovered_endorsements = uncovered_endorsements
        self.uncovered_endorsement_rewards = uncovered_endorsement_rewards
        self.endorsement_deposits = endorsement_deposits
        self.own_block_fees = own_block_fees
        self.extra_block_fees = extra_block_fees
        self.missed_own_block_fees = missed_own_block_fees
        self.missed_extra_block_fees = missed_extra_block_fees
        self.uncovered_own_block_fees = uncovered_own_block_fees
        self.uncovered_extra_block_fees = uncovered_extra_block_fees
        self.double_baking_rewards = double_baking_rewards
        self.double_baking_lost_deposits = double_baking_lost_deposits
        self.double_baking_lost_rewards = double_baking_lost_rewards
        self.double_baking_lost_fees = double_baking_lost_fees
        self.double_endorsing_rewards = double_endorsing_rewards
        self.double_endorsing_lost_deposits = double_endorsing_lost_deposits
        self.double_endorsing_lost_fees = double_endorsing_lost_fees
        self.revelation_rewards = revelation_rewards
        self.revelation_lost_fees = revelation_lost_fees
        self.quote = quote

    def __repr__(self):
        return '<%s %s cycle=%s, staking_balance=%r, num_delegators=%r, delegated_balance=%s, expected_blocks=%s, expected_endorsements=%s>' % (self.__class__.__name__, id(self), self.cycle, self.staking_balance, self.delegated_balance, self.num_delegators, self.expected_blocks, self.expected_endorsements)

    @classmethod
    def from_api(cls, data):
        data = super(Reward, cls).from_api(data)
        cycle = data['cycle']
        staking_balance = data['stakingBalance']
        delegated_balance = data['delegatedBalance']
        num_delegators = data['numDelegators']
        expected_blocks = data['expectedBlocks']
        expected_endorsements = data['expectedEndorsements']
        future_blocks = data['futureBlocks']
        future_block_rewards = data['futureBlockRewards']
        future_block_deposits = data['futureBlockDeposits']
        own_blocks = data['ownBlocks']
        own_block_rewards = data['ownBlockRewards']
        extra_blocks = data['extraBlocks']
        extra_block_rewards = data['extraBlockRewards']
        missed_own_blocks = data['missedOwnBlocks']
        missed_own_block_rewards = data['missedOwnBlockRewards']
        missed_extra_blocks = data['missedExtraBlocks']
        missed_extra_block_rewards = data['missedExtraBlockRewards']
        uncovered_own_blocks = data['uncoveredOwnblocks']
        uncovered_own_block_rewards = data['uncoveredOwnBlockRewards']
        uncovered_extra_blocks = data['uncoveredExtraBlocks']
        uncovered_extra_block_rewards = data['uncoveredExtraBlockRewards']
        block_deposits = data['blockDeposits']
        future_endorsements = data['futureEndorsements']
        future_endorsement_rewards = data['futureEndorsementRewards']
        future_endorsement_deposits = data['futureEndorsementDeposits']
        endorsements = data['endorsements']
        endorsement_rewards = data['endorsementRewards']
        missed_endorsements = data['missedEndorsements']
        missed_endorsement_rewards = data['missedEndorsementRewards']
        uncovered_endorsements = data['uncoveredEndorsements']
        uncovered_endorsement_rewards = data['uncoveredEndorsementRewards']
        endorsement_deposits = data['endorsementDeposits']
        own_block_fees = data['ownBlockFees']
        extra_block_fees = data['extraBlockFees']
        missed_own_block_fees = data['missedOwnBlockFees']
        missed_extra_block_fees = data['missedExtraBlockFees']
        uncovered_own_block_fees = data['uncoveredOwnBlockFees']
        uncovered_extra_block_fees = data['uncoveredExtraBlockFees']
        double_baking_rewards = data['doubleBakingRewards']
        double_baking_lost_deposits = data['doubleBakingLostDeposits']
        double_baking_lost_rewards = data['doubleBakingLostRewards']
        double_baking_lost_fees = data['doubleBakingLostFees']
        double_endorsing_rewards = data['doubleEndorsingRewards']
        double_endorsing_lost_deposits = data['doubleEndorsingLostDeposits']
        double_endorsing_lost_fees = data['doubleEndorsingLostFees']
        revelation_rewards = data['revelationRewards']
        revelation_lost_fees = data['revelationLostFees']
        quote = data['quote']
        return cls(cycle, staking_balance, delegated_balance, num_delegators, expected_blocks, expected_endorsements, future_blocks, future_block_rewards, future_block_deposits, own_blocks, own_block_rewards, extra_blocks, extra_block_rewards, missed_own_blocks, missed_own_block_rewards, missed_extra_blocks, missed_extra_block_rewards, uncovered_own_blocks, uncovered_own_block_rewards, uncovered_extra_blocks, uncovered_extra_block_rewards, block_deposits, future_endorsements, future_endorsement_rewards, future_endorsement_deposits, endorsements, endorsement_rewards, missed_endorsements, missed_endorsement_rewards, uncovered_endorsements, uncovered_endorsement_rewards, endorsement_deposits, own_block_fees, extra_block_fees, missed_own_block_fees, missed_extra_block_fees, uncovered_own_block_fees, uncovered_extra_block_fees, double_baking_rewards, double_baking_lost_deposits, double_baking_lost_rewards, double_baking_lost_fees, double_endorsing_rewards, double_endorsing_lost_deposits, double_endorsing_lost_fees, revelation_rewards, revelation_lost_fees, quote)

    @classmethod
    def baker_count(cls, address, **kwargs):
        path = 'v1/rewards/bakers/%s/count' % address
        response = cls._request(path, **kwargs)
        data = response.content
        return int(data)

    @classmethod
    def by_baker(cls, address, **kwargs):
        path = 'v1/rewards/bakers/%s' % address
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_params = cls.get_comparator_fields(kwargs, ['cycle'], cls.comparator_suffixes)

        params = dict()
        params.update(pagination_params)
        params.update(optional_params)

        quote = kwargs.pop('quote', None)
        if quote:
            params['quote'] = quote

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_baker_cycle(cls, address, cycle, **kwargs):
        path = 'v1/rewards/bakers/%s/%s' % (address, cycle)
        params = dict()

        quote = kwargs.pop('quote', None)
        if quote:
            params['quote'] = quote

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return Reward.from_api(data)

    @classmethod
    def delegator_count(cls, address, **kwargs):
        path = 'v1/rewards/delegators/%s/count' % address
        response = cls._request(path, **kwargs)
        data = response.content
        return int(data)

    @classmethod
    def by_delegator(cls, address, **kwargs):
        path = 'v1/rewards/delegators/%s' % address

        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_params = cls.get_comparator_fields(kwargs, ['cycle'], cls.comparator_suffixes)

        params = dict()
        params.update(pagination_params)
        params.update(optional_params)

        quote = kwargs.pop('quote', None)
        if quote:
            params['quote'] = quote

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_delegator_cycle(cls, address, cycle, **kwargs):
        path = 'v1/rewards/delegators/%s/%s' % (address, cycle)

        quote = kwargs.pop('quote', None)
        if quote:
            params['quote'] = quote

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return Reward.from_api(data)

    @classmethod
    def baker_reward_splits(cls, address, cycle, **kwargs):
        path = 'v1/rewards/split/%s/%s' % (address, cycle)
        params = cls.get_pagination_parameters(kwargs)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return Reward.from_api(data)

    @classmethod
    def reward_splits_delegator(cls, baker, cycle, delegator, **kwargs):
        path = 'v1/rewards/split/%s/%s/%s' % (baker, cycle, delegator)
        response = cls._request(path, **kwargs)
        return response.json()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fetch rewards by address')
    parser.add_argument('-d', '--domain', type=str, default=Reward.domain, help='tzKT domain to fetch data from')
    parser.add_argument('--cycle', type=int, help='Cycle to fetch rewards for')
    parser.add_argument('--limit', type=int, default=10000, help='Max number of rewards to fetch')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--baker', type=str, help='Address of baker')
    group.add_argument('--delegator', type=str, help='Address of delegator')

    args = parser.parse_args()
    kwargs = dict(limit=args.limit, domain=args.domain)
    if args.cycle:
        if args.baker:

            rewards = Reward.by_baker_cycle(args.baker, args.cycle, **kwargs)
        else:
            rewards = Reward.by_delegator_cycle(args.delegator, args.cycle, **kwargs)
    else:
        if args.baker:
            rewards = Reward.by_baker(args.baker, **kwargs)
        else:
            rewards = Reward.by_delegator_cycle(args.delegator, **kwargs)

    for reward in rewards:
        print(reward)
