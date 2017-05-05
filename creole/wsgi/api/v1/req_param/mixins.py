# coding: utf-8
from flask_restful.reqparse import Argument

from creole.util import Enum


class AccountParserMixin:
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
    note = Argument('note', required=False, location=('json', 'form'))
