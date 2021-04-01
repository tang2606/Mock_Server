from flask import request, json

from MockServer.response import VALID, TYPE_NOT_MATCH, EQUALS, NOT_BETWEEN, STR_NOT_CONTAINS, STR_TOO_LONG, MISS, \
    INVALID


def get_response(response, actual):
    return json.dumps(response, ensure_ascii=False) if response else json.dumps(actual, ensure_ascii=False)


class Validator:
    """
    Validator for mock check
    """

    @classmethod
    def valid(cls, response=None):
        return get_response(response, VALID)

    @classmethod
    def type_not_match(cls, type, data, response=None):
        msg = '{data} must be {type} type'.format(data=data, type=type)
        TYPE_NOT_MATCH['msg'] = msg
        if type == 'int':
            if not isinstance(data, int):
                return get_response(response, TYPE_NOT_MATCH)
        elif type == 'float':
            if not isinstance(data, float):
                return get_response(response, TYPE_NOT_MATCH)
        elif type == 'string':
            if not isinstance(data, str):
                return get_response(response, TYPE_NOT_MATCH)
        elif type == 'bool':
            if not isinstance(data, bool):
                return get_response(response, TYPE_NOT_MATCH)
        elif type == 'list':
            if not isinstance(data, list):
                return get_response(response, TYPE_NOT_MATCH)
        elif type == 'dict':
            if not isinstance(data, dict):
                return get_response(response, TYPE_NOT_MATCH)
        else:
            return False

    @classmethod
    def is_not_equals(cls, data, expect, response=None):
        if data != expect:
            msg = '{data} must be equals {expect}'.format(data=data, expect=expect)
            EQUALS['msg'] = msg
            return get_response(response, EQUALS)
        else:
            return False

    @classmethod
    def is_not_between(cls, data, between, response=None):
        try:
            min = between[0]
            max = between[1]
        except IndexError:
            return {'msg': 'mock config error'}
        if data > max or min < min:
            msg = '{data} must be between in {between}'.format(data=data, between=between)
            NOT_BETWEEN['msg'] = msg
            return get_response(response, NOT_BETWEEN)
        else:
            return False

    @classmethod
    def is_not_contains(cls, data, expect, response=None):
        if data not in expect:
            msg = '{data} not in {expect}'.format(data=data, expect=expect)
            STR_NOT_CONTAINS['msg'] = msg
            return get_response(response, STR_NOT_CONTAINS)
        else:
            return False

    @classmethod
    def is_too_long(cls, data, length, response=None):
        if len(data) > length:
            msg = '{data} is  too long, max length is {length}'.format(data=data, length=length)
            STR_TOO_LONG['msg'] = msg
            return get_response(response, STR_TOO_LONG)
        else:
            return False


def domain_server(**kwargs):
    """
    used for POST PUT DELETE
    :param kwargs: standard json mock scripts
    :return: response msg  response
    """
    print('进入domain_server ')
    # data = kwargs.get('data', {})
    data = json.loads(kwargs.get('response'))
    body = json.loads(kwargs.get('body'))

    print("kwargs",kwargs,type(kwargs))


    print("*"*100)
    print(data,type(data))
    print(body, type(body))

    print("*" * 100)


    form = {}
    if request.json:
        form = request.json

    elif request.form:
        form = request.form

    elif request.args:
        form = request.args


    print('12312312312',form,type(form))
    print(body, type(body))

    if data is {}:  # do not have any parameters
        return Validator.valid(response=kwargs.get('body'))

    else:
        if form != body:
            return json.dumps(MISS, ensure_ascii=False)

        else:
            return data

