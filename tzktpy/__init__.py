from . import account
from . import balance
from . import bigmap
from . import block
from . import commitment
from . import contract
from . import cycle
from . import delegate
from . import head
from . import operation
from . import protocol
from . import quote
from . import reward
from . import right
from . import software
from . import statistics
from . import voting

from .base import Base


def home(**kwargs):
    """
    Fetches high-level data about the current state of the Tezos network.

    Keyword Parameters:
        quote (str, optional):  The currency to denominate financial values in.  Defaults to 'usd'.
        domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

    Returns:
        dict: Miscellaneous high-level data about the current state of Tezos network.

    Examples:
        >>> quote = 'btc'
        >>> data = home(quote=quote)
    """
    path = 'v1/home'
    quote = kwargs.pop('quote', 'usd')
    params = dict(quote=quote)
    response = Base._request(path, params=params, **kwargs)
    return response.json()


if __name__ == '__main__':
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Fetch high-level information about the current state of the Tezos network')
    parser.add_argument('--quote', type=str, default='usd', help='currency to quote values in. Defaults to usd')
    parser.add_argument('--domain', type=str, default=Base.domain, help='tzKT domain to fetch data from.  Defaults to api.tzkt.io')

    args = parser.parse_args()
    summary = home(quote=args.quote, domain=args.domain)

    print(json.dumps(summary, indent=4, sort_keys=True))
