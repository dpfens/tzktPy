from .base import Base
__all__ = ('Block', )


class Block(Base):
    __slots__ = ('level', 'hash', 'timestamp', 'proto', 'priority', 'validations', 'deposit', 'reward', 'fees', 'nonce_revealed', 'baker', 'software', 'endorsements', 'proposals', 'ballots', 'activations', 'doubleBaking', 'doubleEndorsing', 'nonceRevelations', 'delegations', 'originations', 'transactions', 'reveals', 'quote')

    def __init__(self, level, hash, timestamp, proto, priority, validations, deposit, reward, fees, nonce_revealed, baker, software, endorsements, proposals, ballots, activations, doubleBaking, doubleEndorsing, nonceRevelations, delegations, originations, transactions, reveals, quote):
        self.level = level
        self.hash = hash
        self.timestamp = timestamp
        self.proto = proto
        self.priority = priority
        self.validations = validations
        self.deposit = deposit
        self.reward = reward
        self.fees = fees
        self.nonce_revealed = nonce_revealed
        self.baker = baker
        self.software = software
        self.endorsements = endorsements
        self.proposals = proposals
        self.ballots = ballots
        self.activations = activations
        self.doubleBaking = doubleBaking
        self.doubleEndorsing = doubleEndorsing
        self.nonceRevelations = nonceRevelations
        self.delegations = delegations
        self.originations = originations
        self.transactions = transactions
        self.reveals = reveals
        self.quote = quote

    def __str__(self):
        return self.hash

    def __repr__(self):
        return '<%s %s level=%i, hash=%r, timestamp=%r, deposit=%r, baker=%r, fees=%r, reward=%r>' % (self.__class__.__name__, id(self), self.level, self.hash, self.timestamp, self.deposit, self.baker, self.fees, self.reward)

    @classmethod
    def from_api(cls, data):
        data = super(Block, cls).from_api(data)
        level = data['level']
        hash = data['hash']
        timestamp = data['timestamp']
        proto = data['proto']
        priority = data['priority']
        validations = data['validations']
        deposit = data['deposit']
        reward = data['reward']
        fees = data['fees']
        nonceRevealed = data['nonceRevealed']
        baker = data['baker']
        software = data['software']
        endorsements = data['endorsements']
        proposals = data['proposals']
        ballots = data['ballots']
        activations = data['activations']
        doubleBaking = data['doubleBaking']
        doubleEndorsing = data['doubleEndorsing']
        nonceRevelations = data['nonceRevelations']
        delegations = data['delegations']
        originations = data['originations']
        transactions = data['transactions']
        reveals = data['reveals']
        quote = data['quote']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        return cls(level, hash, timestamp, proto, priority, validations, deposit, reward, fees, nonceRevealed, baker, software, endorsements, proposals, ballots, activations, doubleBaking, doubleEndorsing, nonceRevelations, delegations, originations, transactions, reveals, quote)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns a list of blocks.

        Keyword Parameters:
            baker (str):  Filters blocks by baker.  Supports standard modifiers.
            level (int):  Filters blocks by level.  Supports standard modifiers.
            timestamp (date|datetime): Filters blocks by timestamp.  Supports standard modifiers.
            priority (int):  Filters blocks by priority.  Supports standard modifiers.
            sort (str):  Sorts blocks by specified field. Supported fields: id (default), level, priority, validations, reward, fees.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list: Blocks matching the given criteria

        Example:
            >>> blocks = Block.get(level__gt=100000)
        """
        path = 'v1/blocks'
        optional_base_params = ['baker', 'level', 'timestamp', 'priority', 'quote'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, incude=optional_base_params)
        response = cls._request(path, params=params)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def by_hash(cls, hash, **kwargs):
        """
        Returns a block with the specified hash.

        Parameters:
            hash (str):  Block hash

        Keyword Parameters:
            operations (bool):  Flag indicating whether to include block operations into returned object or not. Default: False.
            micheline (int):  Format of the parameters, storage and diffs: 0 - JSON, 1 - JSON string, 2 - raw micheline, 3 - raw micheline string.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Block

        Example:
            >>> block_hash = 'sfdf...'
            >>> block = Block.by_hash(block_hash)
        """
        path = 'v1/blocks/%s' % hash
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def by_level(cls, level, **kwargs):
        """
        Returns a block at the specified level.

        Parameters:
            level (int):  Block level

        Keyword Parameters:
            operations (bool):  Flag indicating whether to include block operations into returned object or not. Default: False.
            micheline (int):  Format of the parameters, storage and diffs: 0 - JSON, 1 - JSON string, 2 - raw micheline, 3 - raw micheline string.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Block

        Example:
            >>> block = Block.by_level(150000)
        """
        path = 'v1/blocks/%s' % level
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)

    @classmethod
    def count(cls, **kwargs):
        """
        Returns the total number of blocks.

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Example:
            >>> block_count = Block.count()
        """
        path = 'v1/blocks/count'
        response = cls._request(path)
        value = response.content
        return int(value)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Fetch Block by hash/level')
    parser.add_argument('-d', '--domain', type=str, default=Block.domain, help='tzKT domain to fetch data from')
    parser.add_argument('--gap', type=int, default=2, help='Gap between columns')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--hash', type=str, help='Hash of the desired block')
    group.add_argument('--level', type=str, help='Level of the desired block')
    args = parser.parse_args()

    kwargs = dict(domain=args.domain)
    block_count = Block.count(**kwargs)
    print('Total Blocks: %i' % block_count)

    if args.hash:
        block = Block.by_hash(args.hash, **kwargs)
    else:
        block = Block.by_level(args.level, **kwargs)

    headers = ('Level', 'Hash', 'Timestamp', 'Priority', 'Deposit', 'Reward', 'Fees', 'Baker (Alias)', 'Baker (Address)')
    columns = (block.level, block.hash, block.timestamp.strftime('%Y-%m-%d %H:%M:%S'), block.priority, block.deposit, block.reward, block.fees, block.baker['alias'], block.baker['address'])
    column_formats = []
    for header, value in zip(headers, columns):
        value_length = len(str(value))
        column_width = max(len(header), value_length) + args.gap
        column_format = '{:<%s}' % column_width
        column_formats.append(column_format)

    table_format = ' '.join(column_formats)
    print(table_format.format(*headers))
    message = table_format.format(*columns)
    print(message)
