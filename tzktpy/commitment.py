from .base import Base


class Commitment(Base):
    __slots__ = ('address', 'balance', 'activated', 'activation_level', 'activation_time', 'activated_account')

    def __init__(self, address, balance, activated, activation_level, activation_time, activated_account):
        self.address = address
        self.balance = balance
        self.activated = activated
        self.activation_level = activation_level
        self.activation_time = activation_time
        self.activated_account = activated_account

    def __repr__(self):
        return '<%s %s address=%r, balance=%r, activated=%r, activation_level=%r, activation_time=%r>' % (self.__class__.__name__, id(self), self.address, self.balance, self.activated, self.activation_level, self.activation_time)

    @classmethod
    def from_api(cls, data):
        data = super(Commitment, cls).from_api(data)
        address = data['address']
        balance = data['balance']
        activated = data['activated']
        activation_level = data['activationLevel']
        activation_time = data['activationTime']
        activated_account = data['activatedAccount']
        if activation_time:
            activation_time = cls.to_datetime(activation_time)
        return cls(address, balance, activated, activation_level, activation_time, activated_account)

    @classmethod
    def get(cls, **kwargs):
        path = 'v1/commitments'
        pagination_params = cls.get_pagination_parameters(kwargs)
        optional_base_params = ['activationLevel', 'balance']
        optional_params = cls.get_comparator_fields(kwargs, optional_base_params, cls.comparator_suffixes)

        params = dict()
        params.update(pagination_params)
        params.update(optional_params)
        if 'activated' in kwargs:
            params['activated'] = kwargs.pop('activated')

        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def count(cls, **kwargs):
        path = 'v1/commitments/count'
        optional_base_params = ['balance']
        params = cls.get_comparator_fields(kwargs, optional_base_params, cls.comparator_suffixes)

        if 'activated' in kwargs:
            params['activated'] = kwargs.pop('activated')

        response = cls._request(path, params=params, **kwargs)
        value = response.content
        return int(value)

    @classmethod
    def by_blinded_address(cls, address, **kwargs):
        path = 'v1/commitments/%s' % address
        response = cls._request(path, **kwargs)
        data = response.json()
        return Commitment.from_api(data)


if __name__ == '__main__':
    commitments = Commitment.get()
    print(commitments)
