# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser
from creole.util import Enum


# 餐厅类型
RESTAURANT_TYPE = Enum(
    ('CHINESE', 1, u'中餐'),
    ('WESTERN', 2, u'西餐'),
    ('SPECIAL', 3, u'特色'),
    ('GENERAL', 4, u'综合'),
)


class CreateRestaurantCompanyApiParser(BaseRequestParser):
    name = Argument('name', nullable=False, required=True)
    name_en = Argument('name_en', nullable=False, required=True)

class SearchRestaurantCompanyApiParser(BaseRequestParser):
    is_all = Argument('is_all', type=bool, default=False, required=True)
    name = Argument('name', required=False)
    name_en = Argument('name_en', required=False)


class CreateRestaurantApiParser(BaseRequestParser):
    CURRENCY = Enum(
        ('USD', 1, u'美元'),
        ('CNY', 2, u'人民币'),
        ('LKR', 3, u'斯里兰卡卢布'),
    )

    name = Argument('name', nullable=False, required=True)
    name_en = Argument('name_en', nullable=False, required=True)
    restaurant_type = Argument(
        'restaurant_type', required=True, type=int, nullable=False,
        choices=RESTAURANT_TYPE.values())
    country_id = Argument('country_id', type=int, nullable=False, required=True)
    city_id = Argument('city_id', type=int, nullable=False, required=True)
    company_id = Argument('company_id', type=int, nullable=False, required=True)
    address = Argument('address', nullable=False, required=True)
    contact = Argument('contact', nullable=False, required=True)
    telephone = Argument('telephone', nullable=False, required=True)
    intro_cn = Argument('intro_cn', required=False)
    intro_en = Argument('intro_en', required=False)

    # 支付
    currency = Argument(
        'currency', choices=CURRENCY.values(), type=int, nullable=False,
        required=True, location=('json', 'form'))
    bank_name = Argument('bank_name', nullable=False, required=True, location=('json', 'form'))
    deposit_bank = Argument('deposit_bank', nullable=False, required=True, location=('json', 'form'))
    payee = Argument('payee', nullable=False, required=True, location=('json', 'form'))
    account = Argument('account', nullable=False, required=True, location=('json', 'form'))
    note = Argument('note', required=False, location=('json', 'form'))


class SearchRestaurantApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int, required=False)
    city_id = Argument('city_id', type=int, required=False)
    company_id = Argument('company_id', type=int, required=False)
    restaurant_type = Argument(
        'restaurant_type', required=False, type=int,
        choices=RESTAURANT_TYPE.values())
    page = Argument('page', type=int, default=1, required=False)
    number = Argument('number', type=int, default=20, required=False)


def meal_dict_parser(is_create):
    def wrapper(meal_dict):
        _iter_item = EditMealApiParser._CREATE_PARAM_MAPPING
        if not is_create:
            _iter_item = EditMealApiParser._UPDATE_PARAM_MAPPING

        _meal_dict = {}
        for k, _tuple in _iter_item.iteritems():
            _type, is_required = _tuple
            v = meal_dict.get(k, None)
            if v is None and is_required:
                raise ValueError('Required value: {!r}'.format(k))
            try:
                _meal_dict[k] = _type(v)
            except Exception:
                raise ValueError('Invalid value: {!r}'.format(v))
        return _meal_dict
    return wrapper


class EditMealApiParser(BaseRequestParser):
    TYPE = Enum(
        ('STANDARD', 1, u'标准餐'),
        ('UPGRADE', 2, u'升级餐'),
        ('LUXURY', 3, u'豪华餐'),
    )
    _CREATE_PARAM_MAPPING = {
        'restaurant_id': (int, True),
        'meal_type': (int, True),
        'adult_fee': (float, True),
        'adult_cost': (float, True),
        'child_fee': (float, True),
        'child_cost': (float, True),
    }
    _UPDATE_PARAM_MAPPING = {
        'id': (int, True),
        'adult_fee': (float, False),
        'adult_cost': (float, False),
        'child_fee': (float, False),
        'child_cost': (float, False),
    }

    create_meal_list = Argument(
        'create_meal_list', type=meal_dict_parser(is_create=True),
        required=False, action='append')
    update_meal_list = Argument(
        'update_meal_list', type=meal_dict_parser(is_create=False),
        required=False, action='append')
    delete_id_list = Argument(
        'delete_id_list', type=int, required=False, action='append')
