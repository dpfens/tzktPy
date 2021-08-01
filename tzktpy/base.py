import requests
from datetime import datetime
from collections import defaultdict


class Base(object):
    domain = 'https://api.tzkt.io'
    datetime_format = '%Y-%m-%dT%H:%M:%SZ'
    datetime_ms_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    comparator_notation = '%s__%s'
    comparator_modifier_delimiter = '__'
    comparator_suffixes = ('eq', 'ne', 'gt', 'ge', 'lt', 'le', 'in', 'ni', 'un', 'as', 'null')
    set_suffixes = ('eq', 'any', 'all')
    offset_suffixes = ('el', 'pg', 'cr')
    sort_suffixes = ('asc', 'desc')
    pagination_parameters = ('sort', 'offset', 'limit')

    @classmethod
    def tez(cls, mutez):
        """
        Calculates the number of tez from mutex

        Parameters:
            mutex (int|float):  The number of mutez to be converted

        Returns:
            float:  Number of tez

        Examples:
            >>> 610000
            >>> Balance.tez(61000)
            0.61
        """
        multiplier = 1000000.0
        return mutez / multiplier

    @classmethod
    def prepare_modifiers(cls, parameters, **kwargs):
        include = kwargs.get('include', [])
        exclude = kwargs.get('exclude', [])
        ignore = kwargs.get('ignore', [])
        ignore.append('domain')
        mappings = dict()
        output_params = dict()
        invalid_parameters = []
        keys = list(parameters.keys())
        for parameter in keys:
            param_parts = parameter.split(cls.comparator_modifier_delimiter)
            new_param = '.'.join(param_parts)
            base_param = param_parts[0]
            is_ignore = base_param in ignore
            is_invalid = base_param in exclude or (include and base_param not in include)
            if is_ignore or is_invalid:
                if not is_ignore:
                    invalid_parameters.append(base_param)
                continue
            output_params[new_param] = parameters.pop(parameter)
            mappings.setdefault(base_param, [])
            mappings[base_param].append(new_param)

        if invalid_parameters:
            raise ValueError('The following parameters are invalid: %s' % ', '.join(invalid_parameters))
        return output_params, mappings

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

    @classmethod
    def from_api(cls, data):
        output = defaultdict(lambda: None)
        output.update(data)
        return output
