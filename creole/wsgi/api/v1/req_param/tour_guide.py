# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser
from creole.util import Enum


GUIDE_TYPE = Enum(
    ('INTERNATIONAL', 0, u'国际导游'),
    ('DRIVER', 1, u'司机导游'),
    ('ATTRACTION', 2, u'景点导游'),
    ('TRANSLATOR', 3, u'翻译'),
)

GENDER = Enum(
    ('MALE', 1, u'男性'),
    ('FEMALE', 2, u'女性'),
)


class SearchTourGuideApiParser(BaseRequestParser):
    country_id = Argument('country_id', type=int)
    gender = Argument('gender', type=int, choices=GENDER.values())
    guide_type = Argument('guide_type', type=int, choices=GUIDE_TYPE.values())
    page = Argument('page', type=int, default=1, required=False)
    number = Argument('number', type=int, default=20, required=False)

class CreateTourGuideApiParser(BaseRequestParser):
    CERTIFICATE_TYPE = Enum(
        ('ID', 1, u'身份证'),
        ('PASSPORT', 2, u'护照'),
    )

    guide_type = Argument(
        'guide_type', type=int, choices=GUIDE_TYPE.values(), required=True)
    country_id = Argument('country_id', type=int, required=True)
    name = Argument('name', required=False)
    name_en = Argument('name_en', type=str, required=False)
    gender = Argument('gender', type=int, choices=GENDER.values(), required=True)
    birthday = Argument('birthday', required=True, type=int)
    start_work = Argument('start_work', type=int, required=True)
    language = Argument('language', required=True)
    certificate_type = Argument(
        'certificate_type', type=int, choices=CERTIFICATE_TYPE.values(), required=True)
    certificate_number = Argument('certificate_number', required=True)
    tour_guide_number = Argument('tour_guide_number', required=True)
    passport_country = Argument('passport_country')
    telephone=Argument('telephone', required=True)
    intro = Argument('intro')
    image_hash = Argument('image_hash', required=True)


class CreateTourGuideFeeApiParser(BaseRequestParser):
    CURRENCY = Enum(
        ('USD', 1, u'美元'),
        ('CNY', 2, u'人民币'),
        ('LKR', 3, u'斯里兰卡卢布'),
    )
    SERVICE_TYPE = Enum(
        ('FIXED', 1, u'固定服务费'),
        ('COUNT', 2, u'人头费'),
    )

    tour_guide_id = Argument('tour_guide_id', type=int, required=True)
    currency = Argument('currency', type=int, choices=CURRENCY.values(), required=True)
    base_fee = Argument('base_fee', type=float, required=True)
    service_type = Argument('service_type', type=int, choices=SERVICE_TYPE.values(), required=True)
    service_fee = Argument('service_fee', type=float, required=True)


def account_dict_parser(is_create):
    def wrapper(account_dict):
        _iter_item = EditTourGuideAccountApiParser._CREATE_PARAM_MAPPING
        if not is_create:
            _iter_item = EditTourGuideAccountApiParser._UPDATE_PARAM_MAPPING

        for k, _tuple in _iter_item.iteritems():
            _type, is_required = _tuple
            v = account_dict.get(k, None)
            if v is None and is_required:
                raise ValueError('Required value: {!r}'.format(k))
            try:
                account_dict[k] = _type(v)
            except Exception:
                raise ValueError('Invalid value: {!r}'.format(v))
        return account_dict
    return wrapper


class EditTourGuideAccountApiParser(BaseRequestParser):
    _CREATE_PARAM_MAPPING = {
        'tour_guide_id': (int, True),  # key: (_type, is_required)
        'currency': (int, True),
        'bank_name': (unicode, True),
        'deposit_bank': (unicode, True),
        'payee': (unicode, True),
        'account': (str, True),
        'note': (unicode, False),
    }
    _UPDATE_PARAM_MAPPING = {
        'id': (int, True),
        'currency': (int, True),
        'bank_name': (unicode, True),
        'deposit_bank': (unicode, True),
        'payee': (unicode, True),
        'account': (str, True),
        'note': (unicode, False),
    }

    create_account_list = Argument(
        'create_account_list', type=account_dict_parser(is_create=True),
        required=False, action='append')
    update_account_list = Argument(
        'update_account_list', type=account_dict_parser(is_create=False),
        required=False, action='append')
    delete_id_list = Argument(
        'delete_id_list', type=int, required=False, action='append')
