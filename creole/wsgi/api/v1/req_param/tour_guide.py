# coding: utf-8
from flask_restful.reqparse import Argument

from ...util import BaseRequestParser
from creole.util import Enum


GUIDE_TYPE = Enum(
    ('INTERNATIONAL', 1, u'国际导游'),
    ('DRIVER', 2, u'司机导游'),
    ('ATTRACTION', 3, u'景点导游'),
    ('TRANSLATOR', 4, u'翻译'),
    ('LEADER', 5, u'领队'),
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
    LANGUAGE_LEVEL = Enum(
        ('EXCELLENT', 1, u'熟练'),
        ('VERY_GOOD', 2, u'优秀'),
        ('GOOD', 3, u'良好'),
        ('FAIR', 4, u'及格'),
        ('POOR', 5, u'差'),
    )
    PASSPORT_TYPE = Enum(
        ('TRAVEL', 1, u'旅游签证'),
        ('BUSINESS', 2, u'商务签证'),
        ('WORK', 3, u'工作签证'),
    )

    guide_type = Argument(
        'guide_type', type=int, choices=GUIDE_TYPE.values(), required=True)
    country_id = Argument('country_id', type=int, nullable=False, required=True)
    name = Argument('name', required=False)
    name_en = Argument('name_en', type=str, nullable=False, required=True)
    nickname_en = Argument('nickname_en', type=str, nullable=False, required=True)
    gender = Argument('gender', type=int, choices=GENDER.values(), required=True)
    birthday = Argument('birthday', nullable=False, required=True, type=int)
    start_work = Argument('start_work', type=int, nullable=False, required=True)
    first_language = Argument('first_language', nullable=False, required=True)
    first_language_level = Argument(
        'first_language_level', type=int, choices=LANGUAGE_LEVEL.values(),
        nullable=False, required=True)
    second_language = Argument('second_language', nullable=False, required=True)
    second_language_level = Argument(
        'second_language_level', type=int, choices=LANGUAGE_LEVEL.values(),
        nullable=False, required=True)
    third_language = Argument('third_language', required=False)
    third_language_level = Argument(
        'third_language_level', type=int, choices=LANGUAGE_LEVEL.values(), required=False)
    certificate_type = Argument(
        'certificate_type', type=int, choices=CERTIFICATE_TYPE.values(), required=True)
    certificate_number = Argument('certificate_number', nullable=False, required=True)
    tour_guide_number = Argument('tour_guide_number', nullable=False, required=True)
    passport_country = Argument('passport_country', nullable=False, required=True)
    passport_type = Argument('passport_type', type=int, choices=PASSPORT_TYPE.values(), required=True)
    passport_note = Argument('passport_note', required=False)
    telephone_one=Argument('telephone_one', nullable=False, required=True)
    telephone_two=Argument('telephone_two', required=False)
    email = Argument('email')
    company_id = Argument('company_id', type=int, nullable=False, required=True)
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

        _account_dict = {}
        for k, _tuple in _iter_item.iteritems():
            _type, is_required = _tuple
            v = account_dict.get(k, None)
            if v is None and is_required:
                raise ValueError('Required value: {!r}'.format(k))
            try:
                _account_dict[k] = _type(v)
            except Exception:
                raise ValueError('Invalid value: {!r}'.format(v))
        return _account_dict
    return wrapper


class EditTourGuideAccountApiParser(BaseRequestParser):
    _CREATE_PARAM_MAPPING = {
        'tour_guide_id': (int, True),  # key: (_type, is_required)
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
        'create_account_list', type=account_dict_parser(is_create=True),
        required=False, action='append')
    update_account_list = Argument(
        'update_account_list', type=account_dict_parser(is_create=False),
        required=False, action='append')
    delete_id_list = Argument(
        'delete_id_list', type=int, required=False, action='append')
