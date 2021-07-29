from .base import Base
__all__ = ('Proposal', 'VotingEpoch', 'VotingPeriod', 'PeriodVoter')


class Proposal(Base):
    __slots__ = ('hash', 'initiator', 'first_period', 'last_period', 'epoch', 'upvotes', 'rolls',  'status', 'metadata')

    def __init__(self, hash, initiator, first_period, last_period, epoch, upvotes, rolls,  status, metadata):
        self.hash = hash
        self.initiator = initiator
        self.first_period = first_period
        self.last_period = last_period
        self.epoch = epoch
        self.upvotes = upvotes
        self.rolls = rolls
        self.status = status
        self.metadata = metadata

    def __str__(self):
        return self.hash

    def __repr__(self):
        alias = None
        if self.metadata:
            alias = self.metadata.get('alias')
        return '<%s %s hash=%r, alias=%r, epoch=%r, first_period=%r, last_period=%r, upvotes=%r>' % (self.__class__.__name__, id(self), self.hash, alias, self.epoch, self.first_period, self.last_period, self.upvotes)

    @classmethod
    def suggestions(cls, query, **kwargs):
        path = 'v1/suggest/proposals/%s' % query
        response = cls._request(path, **kwargs)
        return response.json()

    @classmethod
    def from_api(cls, data):
        data = super(Proposal, cls).from_api(data)
        hash = data['hash']
        initiator = data['initiator']
        first_period = data['firstPeriod']
        last_period = data['lastPeriod']
        epoch = data['epoch']
        upvotes = data['upvotes']
        rolls = data['rolls']
        status = data['status']
        metadata = data['metadata']
        return cls(hash, initiator, first_period, last_period, epoch, upvotes, rolls, status, metadata)

    @classmethod
    def get(cls, **kwargs):
        path = 'v1/voting/proposals'
        optional_base_params = ['epoch'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def count(cls, **kwargs):
        path = 'v1/voting/proposals/count'
        response = cls._request(path, **kwargs)
        data = response.content
        return int(data)

    @classmethod
    def by_hash(cls, hash, **kwargs):
        path = 'v1/voting/proposals/%s' % hash
        response = cls._request(path, **kwargs)
        data = response.json()
        return Proposal.from_api(data)


class VotingPeriod(Base):
    __slots__ = ('index', 'epoch', 'first_level', 'start_time', 'last_level', 'end_time', 'kind', 'status', 'total_bakers', 'total_rolls', 'upvotes_quorum', 'proposals_count', 'top_upvotes', 'top_rolls', 'ballot_quorum', 'supermajority', 'yay_ballots', 'yay_rolls', 'nay_ballots', 'nay_rolls', 'pass_ballots', 'pass_rolls')

    def __init__(self, index, epoch, first_level, start_time, last_level, end_time, kind, status, total_bakers, total_rolls, upvotes_quorum, proposals_count, top_upvotes, top_rolls, ballot_quorum, supermajority, yay_ballots, yay_rolls, nay_ballots, nay_rolls, pass_ballots, pass_rolls):
        self.index = index
        self.epoch = epoch
        self.first_level = first_level
        self.start_time = start_time
        self.last_level = last_level
        self.end_time = end_time
        self.kind = kind
        self.status = status
        self.total_bakers = total_bakers
        self.total_rolls = total_rolls
        self.upvotes_quorum = upvotes_quorum
        self.proposals_count = proposals_count
        self.top_upvotes = top_upvotes
        self.top_rolls = top_rolls
        self.ballot_quorum = ballot_quorum
        self.supermajority = supermajority
        self.yay_ballots = yay_ballots
        self.yay_rolls = yay_rolls
        self.nay_ballots = nay_ballots
        self.nay_rolls = nay_rolls
        self.pass_ballots = pass_ballots
        self.pass_rolls = pass_rolls

    def __str__(self):
        return str(self.index)

    def __int__(self):
        return self.int

    def __repr__(self):
        return '<%s %s epoch=%r, index=%r, kind=%r, first_level=%r, last_level=%r, status=%r>' % (self.__class__.__name__, id(self), self.epoch, self.index, self.kind, self.first_level, self.last_level, self.status)

    @classmethod
    def from_api(cls, data):
        data = super(VotingPeriod, cls).from_api(data)
        index = data['index']
        epoch = data['epoch']
        first_level = data['firstLevel']
        start_time = data['startTime']
        last_level = data['lastLevel']
        end_time = data['endTime']
        kind = data['kind']
        status = data['status']
        total_bakers = data['totalBakers']
        total_rolls = data['totalRolls']
        upvotes_quorum = data['upvotesQuorum']
        proposals_count = data['proposalsCount']
        top_upvotes = data['topUpvotes']
        top_rolls = data['topRolls']
        ballot_quorum = data['ballotQuorum']
        supermajority = data['supermajority']
        yay_ballots = data['yayBallots']
        yay_rolls = data['yayRolls']
        nay_ballots = data['nayBallots']
        nay_rolls = data['nayRolls']
        pass_ballots = data['passBallots']
        pass_rolls = data['passRolls']
        if start_time:
            start_time = cls.to_datetime(start_time)

        if end_time:
            end_time = cls.to_datetime(end_time)

        return cls(index, epoch, first_level, start_time, last_level, end_time, kind, status, total_bakers, total_rolls, upvotes_quorum, proposals_count, top_upvotes, top_rolls, ballot_quorum, supermajority, yay_ballots, yay_rolls, nay_ballots, nay_rolls, pass_ballots, pass_rolls)

    @classmethod
    def get(cls, **kwargs):
        path = 'v1/voting/periods'
        params = cls.get_pagination_parameters(kwargs)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_index(cls, index, **kwargs):
        path = 'v1/voting/periods/%s' % index
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def current(cls, **kwargs):
        path = 'v1/voting/periods/current'
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)


class VotingEpoch(Base):
    __slots__ = ('index', 'first_level', 'start_time', 'last_level', 'end_time', 'status', 'periods', 'proposals')

    def __init__(self, index, first_level, start_time, last_level, end_time, status, periods, proposals):
        self.index = index
        self.first_level = first_level
        self.start_time = start_time
        self.last_level = last_level
        self.end_time = end_time
        self.status = status
        self.periods = periods
        self.proposals = proposals

    def __str__(self):
        return str(self.index)

    def __int__(self):
        return self.int

    def __repr__(self):
        return '<%s %s index=%r, first_level=%r, last_level=%r, status=%r>' % (self.__class__.__name__, id(self), self.index, self.first_level, self.last_level, self.status)

    @classmethod
    def from_api(cls, data):
        data = super(VotingEpoch, cls).from_api(data)
        index = data['index']
        first_level = data['firstLevel']
        start_time = data['startTime']
        last_level = data['lastLevel']
        end_time = data['endTime']
        status = data['status']
        periods = data['periods']
        proposals = data['proposals']
        if start_time:
            start_time = cls.to_datetime(start_time)
        if end_time:
            end_time = cls.to_datetime(end_time)

        if periods:
            periods = [VotingPeriod.from_api(item) for item in periods]

        if proposals:
            proposals = [Proposal.from_api(item) for item in proposals]
        return cls(index, first_level, start_time, last_level, end_time, status, periods, proposals)

    @classmethod
    def get(cls, **kwargs):
        path = 'v1/voting/epochs'
        params = cls.get_pagination_parameters(kwargs)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_index(cls, index, **kwargs):
        path = 'v1/voting/epochs/%s' % index
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def current(cls, **kwargs):
        path = 'v1/voting/epochs/current'
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def latest(cls, **kwargs):
        path = 'v1/voting/epochs/latest_voting'
        response = cls._request(path, **kwargs)
        data = response.json()
        return VotingEpoch.from_api(data)


class PeriodVoter(Base):
    __slots__ = ('delegate', 'rolls', 'status')

    def __init__(self, delegate, rolls, status):
        self.delegate = delegate
        self.rolls = rolls
        self.status = status

    def __str__(self):
        print(self.delegate)
        return str(self.delegate)

    def __repr__(self):
        return '<%s %s delegate=%r, rolls=%r, status=%r>' % (self.__class__.__name__, id(self), self.delegate, self.rolls, self.status)

    @classmethod
    def from_api(cls, data):
        delegate = data['delegate']
        rolls = data['rolls']
        status = data['status']
        return cls(delegate, rolls, status)

    @classmethod
    def get(cls, index, **kwargs):
        path = 'v1/voting/periods/%s/voters' % index
        params = cls.get_pagination_parameters(kwargs)
        status = kwargs.pop('status', None)
        if status:
            params['status'] = status
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_address(cls, index, address, **kwargs):
        path = 'v1/voting/periods/%s/voters/%s' % (index, address)
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def current(cls, **kwargs):
        path = 'v1/voting/periods/current/voters'
        params = cls.get_pagination_parameters(kwargs)
        status = kwargs.pop('status', None)
        if status:
            params['status'] = status
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def current_by_address(cls, address, **kwargs):
        path = 'v1/voting/periods/current/voters/%s' % address
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)


if __name__ == '__main__':
    current_epoch = VotingEpoch.current()
    current_period = VotingPeriod.current()
    current_proposals = Proposal.get(epoch=current_epoch)
    sorted_proposals = sorted(current_proposals, key=lambda x: x.upvotes, reverse=True)

    print('Current proposals during epoch #%s' % current_epoch)
    for proposal in sorted_proposals:
        print('%r' % proposal)

    print()
    voters = PeriodVoter.current()
    if voters:
        print('Voters during period #%s:' % current_period)
        for voter in voters:
            print('%r' % voter)
    else:
        print('No voters during period #%s' % current_period)
