from .base import Base
__all__ = ('Commitment', )


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
        """
        Returns a list of commitments.

        Keyword Parameters:
            activated (bool):  Filters commitments by activation status
            activationLevel (int):  Filters commitments by activation level.  Supports standard modifiers.
            balance (int):  Filters commitments by activated balance.  Supports standard modifiers.
            sort (str):  Sorts delegators by specified field. Supported fields: id (default), balance, activationLevel.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list:  Commitments meeting the specified criteria

        Example:
            >>> commitments = Commitment.get(activated=True, balance__gt=100)
        """
        path = 'v1/commitments'
        optional_base_params = ['activationLevel', 'balance'] + list(cls.pagination_parameters)
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def count(cls, **kwargs):
        """
        Returns a number of commitments.

        Keyword Parameters:
            activated (bool):  Filters commitments by activation status
            balance (int):  Filters commitments by activated balance.  Supports standard modifiers.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int

        Example:
            >>> commitment_count = Commitment.count(activated=True, balance__gt=100)
        """
        path = 'v1/commitments/count'
        optional_base_params = ['balance']
        params, _ = cls.prepare_modifiers(kwargs, include=optional_base_params)
        response = cls._request(path, params=params, **kwargs)
        value = response.content
        return int(value)

    @classmethod
    def by_blinded_address(cls, address, **kwargs):
        """
        Returns a commitment with the specified blinded address.

        Parameters:
            address (str):  A blinded address

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            Commitment

        Example:
            >>> blinded_address = 'tz'
            >>> commitment = Commitment.by_blinded_address(blinded_address)
        """
        path = 'v1/commitments/%s' % address
        response = cls._request(path, **kwargs)
        data = response.json()
        return Commitment.from_api(data)


if __name__ == '__main__':
    commitment_count = Commitment.count()
    print('Total commitments: %r' % commitment_count)
    commitments = Commitment.get()
    print(commitments)
