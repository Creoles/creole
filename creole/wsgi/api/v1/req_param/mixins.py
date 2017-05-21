# coding: utf-8
from flask_restful.reqparse import Argument

from creole.util import Enum


class AccountParserMixin(object):
    CURRENCY = Enum(
        ('USD', 1, u'美元'),
        ('CNY', 2, u'人民币'),
        ('LKR', 3, u'斯里兰卡卢布'),
    )

    currency = Argument(
        'currency', choices=CURRENCY.values(), type=int, nullable=False,
        required=True, location=('json', 'form'))
    bank_name = Argument('bank_name', nullable=False, required=True, location=('json', 'form'))
    deposit_bank = Argument('deposit_bank', nullable=False, required=True, location=('json', 'form'))
    payee = Argument('payee', nullable=False, required=True, location=('json', 'form'))
    account = Argument('account', nullable=False, required=True, location=('json', 'form'))
    swift_code = Argument('swift_code', required=False, location=('json', 'form'))
    note = Argument('note', required=False, location=('json', 'form'))


class ContactParserMixin(object):
    contact = Argument('contact', required=True, nullable=False)
    position = Argument('position', required=True, nullable=False)
    telephone = Argument('telephone', required=True, nullable=False)
    email = Argument('email', required=True, nullable=False)


class CompanyParserMixin(object):
    country_id = Argument(
        'country_id', type=int, nullable=False, required=True)
    city_id = Argument('city_id', type=int, nullable=False, required=True)
    name = Argument('name', nullable=False, required=True)
    name_en = Argument('name_en', nullable=False, required=True)
    nickname_en = Argument('nickname_en', nullable=False, required=True)
    register_number = Argument('register_number', nullable=False, required=True)


def dict_parser_func(param_mapping):
    def wrapper(item_dict):
        _item_dict = {}
        for k, _tuple in param_mapping.iteritems():
            _type, is_required = _tuple
            v = item_dict.get(k, None)
            if v is None and is_required:
                raise ValueError('Required value: {!r}'.format(k))
            try:
                _item_dict[k] = _type(v)
            except Exception:
                raise ValueError('Invalid value: {!r}'.format(v))
        return _item_dict
    return wrapper
