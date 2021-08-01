from .base import Base
__all__ = ('Head', )


class Head(Base):
    __slots__ = ('cycle', 'level', 'hash', 'protocol', 'timestamp', 'voting_epoch', 'voting_period', 'known_level', 'last_sync', 'synced', 'quote_level', 'quote_btc', 'quote_eur', 'quote_usd', 'quote_cny', 'quote_jpy', 'quote_krw', 'quote_eth')

    def __init__(self, cycle, level, hash, protocol, timestamp, voting_epoch, voting_period, known_level, last_sync, synced, quote_level, quote_btc, quote_eur, quote_usd, quote_cny, quote_jpy, quote_krw, quote_eth):
        self.cycle = cycle
        self.level = level
        self.hash = hash
        self.protocol = protocol
        self.timestamp = timestamp
        self.voting_epoch = voting_epoch
        self.voting_period = voting_period
        self.known_level = known_level
        self.last_sync = last_sync
        self.synced = synced
        self.quote_level = quote_level
        self.quote_btc = quote_btc
        self.quote_eur = quote_eur
        self.quote_usd = quote_usd
        self.quote_cny = quote_cny
        self.quote_jpy = quote_jpy
        self.quote_krw = quote_krw
        self.quote_eth = quote_eth

    def __repr__(self):
        return '<%s %s cycle=%r, level=%r, hash=%r, protocol=%r, timestamp=%s, usd=%r>' % (self.__class__.__name__, id(self), self.cycle, self.level, self.hash, self.protocol, self.timestamp, self.quote_usd)

    @classmethod
    def from_api(cls, data):
        cycle = data['cycle']
        level = data['level']
        hash = data['hash']
        protocol = data['protocol']
        timestamp = data['timestamp']
        voting_epoch = data['votingEpoch']
        voting_period = data['votingPeriod']
        known_level = data['knownLevel']
        last_sync = data['lastSync']
        synced = data['synced']
        quote_level = data['quoteLevel']
        quote_btc = data['quoteBtc']
        quote_eur = data['quoteEur']
        quote_usd = data['quoteUsd']
        quote_cny = data['quoteCny']
        quote_jpy = data['quoteJpy']
        quote_krw = data['quoteKrw']
        quote_eth = data['quoteEth']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        if last_sync:
            last_sync = cls.to_datetime(last_sync)
        return cls(cycle, level, hash, protocol, timestamp, voting_epoch, voting_period, known_level, last_sync, synced, quote_level, quote_btc, quote_eur, quote_usd, quote_cny, quote_jpy, quote_krw, quote_eth)

    @classmethod
    def get(cls, **kwargs):
        """
        Returns indexer head and synchronization status.

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Head

        Examples:
            >>> current_head = Head.get()
        """
        path = 'v1/head'
        response = cls._request(path, **kwargs)
        data = response.json()
        return cls.from_api(data)


if __name__ == '__main__':
    head = Head.get()
    message_format = '{:<8} {:<10} {:<11}'
    header = message_format.format('Cycle', 'Level', 'USD')
    print(header)
    formatted_message = message_format.format(head.cycle, head.level, head.quote_usd)
    print(formatted_message)
