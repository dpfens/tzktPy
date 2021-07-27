from .base import Base


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

        Returns:
            list: time series with historical balances (only changes, without duplicates).

        {@link https://api.tzkt.io/#operation/Accounts_GetBalanceHistory | get balance history }.

        Example:
            >>> address = 'tz_1WEHHVMWxQUtkWAgrJBFGXjJ5YqZVgfPVE'
            >>> steps = 100
            >>> balance_history = Balance.history(address, steps=steps)
        """
        path = 'v1/accounts/%s/balance_history' % address
        response = cls._request(path)
        data = response.json()
        output = [cls.from_api(item) for item in data]
        return output

    @classmethod
    def by_level(cls, address, level, **kwargs):
        path = 'v1/accounts/%s/balance_history/%s' % (address, level)
        response = cls._request(path)
        data = response.content
        return data

    @classmethod
    def by_date(cls, address, date, **kwargs):
        date_string = date.isoformat()
        path = 'v1/accounts/%s/balance_history/%s' % (address, date_string)
        response = cls._request(path)
        data = response.content
        return data

    @classmethod
    def report(cls, address, **kwargs):
        delimiter_lookup = dict(comma=b',', semicolon=b';')
        delimiter = kwargs.pop('delimiter', 'comma')
        if delimiter not in delimiter_lookup:
            raise ValueError('%r is not a valid delimiter' % delimiter)
        params = dict(delimiter=delimiter)
        timestamp_params = cls.get_comparator_fields(kwargs, ['from', 'to'], cls.comparator_suffixes)
        for param in timestamp_params:
            value = timestamp_params[param]
            params[param] = value.isoformat()

        optional_params = ('historical', 'currency')
        for param in optional_params:
            if param in kwargs:
                params[param] = kwargs.pop(param)
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
