from .base import Base
__all__ = ('Software', )


class Software(Base):
    __slots__ = ('short_hash', 'first_level', 'first_time', 'last_level', 'last_time', 'blocks_count', 'metadata')

    def __init__(self, short_hash, first_level, first_time, last_level, last_time, blocks_count, metadata):
        self.short_hash = short_hash
        self.first_level = first_level
        self.first_time = first_time
        self.last_level = last_level
        self.last_time = last_time
        self.blocks_count = blocks_count
        self.metadata = metadata

    def __repr__(self):
        version = None
        if self.metadata and 'version' in self.metadata:
            version = self.metadata['version']
        return '<%s %s short_hash=%r, version=%r, first_level=%r, last_level=%r, block_count=%r>' % (self.__class__.__name__, id(self), self.short_hash, version, self.first_level, self.last_level, self.blocks_count)

    @classmethod
    def from_api(cls, data):
        data = super(Software, cls).from_api(data)
        shortHash = data['shortHash']
        firstLevel = data['firstLevel']
        firstTime = data['firstTime']
        lastLevel = data['lastLevel']
        lastTime = data['lastTime']
        blocksCount = data['blocksCount']
        metadata = data['metadata']
        if firstTime:
            firstTime = cls.to_datetime(firstTime)
        if lastTime:
            lastTime = cls.to_datetime(lastTime)
        return cls(shortHash, firstLevel, firstTime, lastLevel, lastTime, blocksCount, metadata)

    @classmethod
    def get(cls, **kwargs):
        path = 'v1/software'
        params = cls.get_pagination_parameters(kwargs)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def count(cls, **kwargs):
        path = 'v1/software/count'
        response = cls._request(path)
        data = response.content
        return int(data)


if __name__ == '__main__':
    software_count = Software.count()
    print('Software count: %i' % software_count)
    software = Software.get()
    for item in software:
        print(item)
