# coding: utf-8
from flask_restful.reqparse import Argument

from creole.util import Enum
from ...util import BaseRequestParser
from .mixins import dict_parser_func


# 餐厅类型
RESTAURANT_TYPE = Enum(
    ('CHINESE', 1, u'中餐'),
    ('SRILANKA', 2, u'斯里兰卡'),
    ('WESTERN', 3, u'西餐'),
    ('SPECIAL', 4, u'综合'),
    ('GENERAL', 5, u'其他'),
)


class CreateRestaurantApiParser(BaseRequestParser):
    ENVIRON_LEVEL = Enum(
        ('EXCELLENT', 1, u'卓越'),
        ('VERY_GOOD', 2, u'非常好'),
        ('GOOD', 3, u'好'),
        ('NORMAL', 4, u'一般'),
        ('POOR', 5, u'差'),
    )
    TASTE_LEVEL = Enum(
        ('EXCELLENT', 1, u'卓越'),
        ('VERY_GOOD', 2, u'非常好'),
        ('GOOD', 3, u'好'),
        ('NORMAL', 4, u'一般'),
        ('POOR', 5, u'差'),
    )
    SERVICE_LEVEL = Enum(
        ('EXCELLENT', 1, u'卓越'),
        ('VERY_GOOD', 2, u'非常好'),
        ('GOOD', 3, u'好'),
        ('NORMAL', 4, u'一般'),
        ('POOR', 5, u'差'),
    )
    COST_LEVEL = Enum(
        ('LUXURY', 1, u'昂贵'),
        ('NORMAL', 2, u'一般'),
        ('BUDGET', 3, u'便宜'),
    )
    COOPERATION_LEVEL = Enum(
        ('KEY', 1, u'核心'),
        ('NORMAL', 2, u'一般'),
    )
    RECOMMEND_LEVEL = Enum(
        ('EXCELLENT', 1, u'卓越'),
        ('VERY_GOOD', 2, u'非常好'),
        ('GOOD', 3, u'好'),
        ('NORMAL', 4, u'一般'),
        ('POOR', 5, u'差'),
    )

    name = Argument('name', nullable=False, required=True)
    name_en = Argument('name_en', nullable=False, required=True)
    nickname_en = Argument('nickname_en', nullable=False, required=True)
    restaurant_type = Argument(
        'restaurant_type', required=True, type=int, nullable=False,
        choices=RESTAURANT_TYPE.values())
    country_id = Argument('country_id', type=int, nullable=False, required=True)
    city_id = Argument('city_id', type=int, nullable=False, required=True)
    address = Argument('address', nullable=False, required=True)
    environ_level = Argument(
        'environ_level', type=int, required=True, choices=ENVIRON_LEVEL.values())
    taste_level = Argument(
        'taste_level', type=int, required=True, choices=TASTE_LEVEL.values())
    service_level = Argument(
        'service_level', type=int, required=True, choices=SERVICE_LEVEL.values())
    cost_level = Argument(
        'cost_level', type=int, required=True, choices=COST_LEVEL.values())
    cooperation_level = Argument(
        'cooperation_level', type=int, required=True, choices=COOPERATION_LEVEL.values())
    recommend_level = Argument(
        'recommend_level', type=int, required=True, choices=RECOMMEND_LEVEL.values())
    contact_one = Argument('contact_one', nullable=False, required=True)
    position_one = Argument('position_one', nullable=False, required=True)
    telephone_one = Argument('telephone_one', nullable=False, required=True)
    email_one = Argument('email_one', nullable=False, required=True)
    contact_two = Argument('contact_two', nullable=False, required=True)
    position_two = Argument('position_two', nullable=False, required=True)
    telephone_two = Argument('telephone_two', nullable=False, required=True)
    email_two = Argument('email_two', nullable=False, required=True)
    contact_three = Argument('contact_three')
    position_three = Argument('position_three')
    telephone_three = Argument('telephone_three')
    email_three = Argument('email_three')
    standard_meal_intro_cn = Argument('standard_meal_intro_cn')
    standard_meal_intro_en = Argument('standard_meal_intro_en')
    upgrade_meal_intro_cn = Argument('upgrade_meal_intro_cn')
    upgrade_meal_intro_en = Argument('upgrade_meal_intro_en')
    luxury_meal_intro_cn = Argument('luxury_meal_intro_cn')
    luxury_meal_intro_en = Argument('luxury_meal_intro_en')
    intro_cn = Argument('intro_cn', required=False)
    intro_en = Argument('intro_en', required=False)


class EditRestaurantAccountApiParser(BaseRequestParser):
    _CREATE_PARAM_MAPPING = {
        'restaurant_id': (int, True),  # key: (_type, is_required)
        'currency': (int, True),
        'bank_name': (unicode, True),
        'deposit_bank': (unicode, True),
        'payee': (unicode, True),
        'account': (str, True),
        'swift_code': (str, False),
        'note': (unicode, False),
    }
    _UPDATE_PARAM_MAPPING = {
        'id': (int, True),
        'currency': (int, True),
        'bank_name': (unicode, True),
        'deposit_bank': (unicode, True),
        'payee': (unicode, True),
        'account': (str, True),
        'swift_code': (str, False),
        'note': (unicode, False),
    }

    create_account_list = Argument(
        'create_account_list',
        type=dict_parser_func(param_mapping=_CREATE_PARAM_MAPPING),
        required=False, action='append')
    update_account_list = Argument(
        'update_account_list',
        type=dict_parser_func(param_mapping=_UPDATE_PARAM_MAPPING),
        required=False, action='append')
    delete_id_list = Argument(
        'delete_id_list', type=int, required=False, action='append')


class SearchRestaurantApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int, required=False)
    city_id = Argument('city_id', type=int, required=False)
    restaurant_type = Argument(
        'restaurant_type', required=False, type=int,
        choices=RESTAURANT_TYPE.values())
    page = Argument('page', type=int, default=1, required=False)
    number = Argument('number', type=int, default=20, required=False)


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
        'create_meal_list',
        type=dict_parser_func(param_mapping=_CREATE_PARAM_MAPPING),
        required=False, action='append')
    update_meal_list = Argument(
        'update_meal_list',
        type=dict_parser_func(param_mapping=_UPDATE_PARAM_MAPPING),
        required=False, action='append')
    delete_id_list = Argument(
        'delete_id_list', type=int, required=False, action='append')
