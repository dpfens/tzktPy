from .base import Base
__all__ = ('BalanceShort', 'Balance')


class BalanceShort(object):
    __slots__ = ('btc', 'usd', 'eth', 'eur', 'cny', 'jpy', 'krw')

    def __init__(self, btc, usd, eth, eur, cny, jpy, krw):
        self.btc = btc
        self.usd = usd
        self.eth = eth
        self.eur = eur
        self.cny = cny
        self.jpy = jpy
        self.krw = krw

    @classmethod
    def from_api(cls, data):
        btc = data['btc']
        usd = data['usd']
        eth = data['eth']
        eur = data['eur']
        cny = data['cny']
        jpy = data['jpy']
        krw = data['krw']
        return cls(btc, usd, eth, eur, cny, jpy, krw)


class Balance(Base):
    __slots__ = ('balance', 'level', 'quote', 'timestamp')

    def __init__(self, balance, level, quote, timestamp):
        self.balance = balance
        self.level = level
        self.quote = quote
        self.timestamp = timestamp

    @classmethod
    def from_api(cls, data):
        balance = data['balance']
        if balance:
            balance = BalanceShort.from_api(balance)
        level = data['level']
        quote = data['quote']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        return cls(balance, level, quote, timestamp)

    @classmethod
    def history(cls, address, **kwargs):
        """
        Fetches balance history of an account from {@link https://tzkt.io/ | tz_KT }.

        Parameters:
            address (str):  The address of a given account

        Keyword Parameters:
            step (int):  Step of the time series, for example if step = 1000 you will get balances at blocks 1000, 2000, 3000, ....
            sort (str):  Sorts historical balances by specified field. Supported fields: level.  Supports sorting modifiers.
            offset (int):  Specifies which or how many items should be skipped. Supports standard offset modifiers.
            limit (int):  Maximum number of items to return.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list: time series with historical balances (only changes, without duplicates).

        Example:
            >>> address = 'tz_1WEHHVMWxQUtkWAgrJBFGXjJ5YqZVgfPVE'
            >>> steps = 100
            >>> balance_history = Balance.history(address, steps=steps)
        """
        path = 'v1/accounts/%s/balance_history' % address
        optional_base_params = ['step'] + list(cls.pagination_parameters)
        params = cls.prepare_modifiers(kwargs, include=optional_base_params)
        response = cls._request(path, params=params, **kwargs)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_level(cls, address, level, **kwargs):
        """
        Fetches balance of a given account at a given level.

        Parameters:
            address (str):  The address of a given account
            level (int): The level at which to get a balance.

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int: balance of the given account at the given level.

        Example:
            >>> address = 'tz1WEHHVMWxQUtkWAgrJBFGXjJ5YqZVgfPVE'
            >>> level = 100000
            >>> balance = Balance.by_level(address, level)
        """
        path = 'v1/accounts/%s/balance_history/%s' % (address, level)
        response = cls._request(path)
        data = response.content
        return data

    @classmethod
    def by_date(cls, address, date, **kwargs):
        """
        Fetches balance of a given account at a given date.

        Parameters:
            address (str):  The address of a given account
            date (date|datetime): The date at which to get a balance.

        Keyword Parameters:
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            int: balance of the given account at the given account date.

        Example:
            >>> address = 'tz1WEHHVMWxQUtkWAgrJBFGXjJ5YqZVgfPVE'
            >>> date = datetime.date(2020, 3, 17)
            >>> balance = Balance.by_date(address, date)
        """
        date_string = date.isoformat()
        path = 'v1/accounts/%s/balance_history/%s' % (address, date_string)
        response = cls._request(path)
        data = response.content
        return data

    @classmethod
    def report(cls, address, **kwargs):
        """
        Fetches a report on the balances of the given address.

        Parameters:
            address (str):  The address of a given account

        Keyword Parameters:
            from (date|datetime):  Start of the time range to filter by.  Supports standard modifiers.
            to (date|datetime):  End of the time range to filter by.  Supports standard modifiers.
            currency:  Currency to convert amounts to (btc, eur, usd, cny, jpy, krw, eth).
            historical (bool):  Indicates if you want to use historical prices. Defaults to false.
            domain (str, optional):  The tzkt.io domain to use.  The domains correspond to the different Tezos networks.  Defaults to https://api.tzkt.io.

        Returns:
            list: A list of account balances as delimited lists.

        Example:
            >>> address = 'tz1WEHHVMWxQUtkWAgrJBFGXjJ5YqZVgfPVE'
            >>> balance = Balance.report(address)
        """
        delimiter_lookup = dict(comma=b',', semicolon=b';')
        delimiter = kwargs.pop('delimiter', 'comma')
        if delimiter not in delimiter_lookup:
            raise ValueError('%r is not a valid delimiter' % delimiter)
        params, _ = cls.prepare_modifiers(kwargs, include=('from', 'to'))
        params['delimiter'] = delimiter

        path = 'v1/accounts/%s/report' % address
        response = cls._request(path, params=params, **kwargs)
        raw_csv = response.content
        delimiter = delimiter_lookup[delimiter]
        output = []
        for line in raw_csv.split(b'\n'):
            cells = line.split(delimiter)
            if not any(cells):
                break
            output.append(cells)
        return output


if __name__ == '__main__':
    import argparse
    import csv
    from datetime import datetime

    parser = argparse.ArgumentParser(description='Fetch balance report by Tezos account address')
    parser.add_argument('-a', '--address', type=str, help='Address of account to report on')
    parser.add_argument('-s', '--start', type=str, help='Start date of the balance report (YYYY-MM-DD)')
    parser.add_argument('-t', '--to', type=str, help='End date of the balance report (YYYY-MM-DD)')
    parser.add_argument('--historical', action='store_true', help='Use historical prices instead of current price')
    parser.add_argument('-c', '--currency', type=str, help='Currency to convert amounts to')
    parser.add_argument('-o', '--output', type=str, help='File path of the produced report')
    parser.add_argument('--domain', type=str, default=Balance.domain, help='tzKT domain to fetch data from')
    date_format = '%Y-%m-%d'

    args = parser.parse_args()
    kwargs = dict(domain=args.domain)
    if args.start:
        start_date = datetime.strptime(args.start, date_format)
        kwargs['from'] = start_date

    if args.to:
        to_date = datetime.strptime(args.to, date_format)
        kwargs['to'] = to_date

    if args.currency:
        kwargs['currency'] = args.currency
    raw_report = Balance.report(args.address, **kwargs)
    if raw_report:
        if args.output:
            with open(args.output, 'w') as output_file:
                writer = csv.writer(output_file)
                for row in raw_report:
                    row = [value.decode('utf-8') for value in row]
                    writer.writerow(row)
        else:
            # find the maximum width of each column
            columns = [len(cell) for cell in raw_report[0]]
            for row in raw_report:
                for index, cell in enumerate(row):
                    columns[index] = max(columns[index], len(cell))

            column_formats = ['{:<%s}' % column for column in columns]
            format_str = ' '.join(column_formats)
            for row in raw_report:
                str_row = [value.decode('utf-8') for value in row]
                formatted_row = format_str.format(*str_row)
                print(formatted_row)
