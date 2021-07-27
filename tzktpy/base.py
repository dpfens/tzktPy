import requests
from datetime import datetime
from collections import defaultdict


class Base(object):
    domain = 'https://api.tzkt.io'
    datetime_format = '%Y-%m-%dT%H:%M:%SZ'
    datetime_ms_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    comparator_notation = '%s__%s'
    comparator_suffixes = ('eq', 'ne', 'gt', 'ge', 'lt', 'le', 'in', 'ni', 'un', 'as', 'null')
    set_suffixes = ('eq', 'any', 'all')
    offset_suffixes = ('el', 'pg', 'cr')
    sort_suffixes = ('asc', 'desc')

    @classmethod
    def get_comparator_fields(cls, parameters, fields, suffixes):
        output = dict()
        for field in fields:
            if field in parameters:
                output[field] = parameters.pop(field)
                continue

            for suffix in suffixes:
                field_name = cls.comparator_notation % (field, suffix)
                if field_name in parameters:
                    output['%s.%s' % (field, suffix)] = parameters.pop(field_name)

        return output

    @classmethod
    def get_multicomparator_fields(cls, parameters, fields, suffixes):
        output = dict()
        for field in fields:
            if field in parameters:
                values = parameters.pop(field)
                output[field] = ','.join(values)
                continue

            for suffix in suffixes:
                field_name = cls.comparator_notation % (field, suffix)
                if field_name in parameters:
                    values = parameters.pop(field_name)
                    output['%s.%s' % (field, suffix)] = ','.join(values)

        return output

    @classmethod
    def get_pagination_parameters(cls, parameters):
        pagination_params = {
            'sort': cls.sort_suffixes,
            'offset': cls.offset_suffixes,
            'limit': ()
        }
        output = dict()
        for field in pagination_params:
            if field in parameters:
                output[field] = parameters.pop(field)
                continue

            suffixes = pagination_params[field]
            for suffix in suffixes:
                field_name = cls.comparator_notation % (field, suffix)
                if field_name in parameters:
                    output['%s.%s' % (field, suffix)] = parameters.pop(field_name)
        return output

    @classmethod
    def setdefaults(cls, parameters):
        parameters.setdefault('domain', cls.domain)
        parameters.setdefault('method', 'GET')
        return parameters

    @classmethod
    def validate_request_parameters(cls, parameters):
        valid_parameters = set(['domain', 'method', 'params', 'json', 'data'])
        included_parameters = set(parameters)
        invalid_parameters = included_parameters - valid_parameters
        if invalid_parameters:
            raise ValueError('The following parameters are invalid: %r' % (invalid_parameters, ))

    @classmethod
    def _request(cls, path, **kwargs):
        cls.validate_request_parameters(kwargs)
        kwargs = cls.setdefaults(kwargs)
        domain = kwargs.pop('domain')
        method = kwargs.pop('method')
        url = '%s/%s' % (domain, path)
        response = requests.request(method, url, **kwargs)
        return response

    @classmethod
    def to_datetime(cls, text):
        formats = [cls.to_datetime, cls.datetime_format]
        for format in formats:
            try:
                value = datetime.strptime(text, cls.datetime_format)
            except Exception:
                pass
            else:
                return value
        return None

    def from_api(data):
        output = defaultdict(lambda: None)
        output.update(data)
        return output
