# coding: utf-8
class BaseCreoleErrCode(object):
    """Some general error code."""
    # unknown error
    UNKNOWN_SYSTEM_ERROR = 1001

    # database error
    DATABASE_ERROR = 1101

    # service error
    VALIDATION_ERROR = 2001
    PARAMETER_ERROR = 2002

    # client error
    USER_NAME_DUPLICATED = 3001
    USER_NOT_EXIST = 3002

    # 国家和城市
    COUNTRY_NAME_DUPLICATED = 3010
    CITY_NAME_DUPLICATED = 3011
    COUNTRY_NOT_EXIST = 3012
    CITY_NOT_EXIST = 3013

    # 购物店
    SHOP_NOT_EXIST = 3020
    SHOP_COMPANY_DUPLICATED = 3021
    SHOP_COMPANY_NOT_EXIST = 3022

    # 车辆
    VEHICLE_COMPANY_DUPLICATED = 3030
    VEHICLE_COMPANY_NOT_EXIST = 3031
    VEHICLE_NOT_EXIST = 3032
    # 车辆结算
    VEHICLE_ACCOUNT_NOT_EXIST = 3033

    # 景点
    ATTRACTION_NOT_EXIST = 3040

    # 餐饮
    RESTAURANT_COMPANY_NOT_EXIST = 3050
    RESTAURANT_COMPANY_DUPLICATED = 3051
    RESTAURANT_NOT_EXIST = 3052
    RESTAURANT_MEAL_REACH_LIMIT = 3053
    RESTAURANT_MEAL_TYPE_NOT_EXIST = 3054

    # 导游
    TOUR_GUIDE_NOT_EXIST = 3060
    TOUR_GUIDE_ID_DUPLICATED = 3061
    TOUR_GUIDE_ACCOUNT_NOT_EXIST = 3062
    TOUR_GUIDE_ACCOUNT_DUPLICATED = 3063
    TOUR_GUIDE_FEE_NOT_EXIST = 3064

class CreoleErrCode(BaseCreoleErrCode):
    pass


TRANSLATIONS = {
    200: u'ok',
    CreoleErrCode.UNKNOWN_SYSTEM_ERROR: u'unknown system error',

    # database error
    CreoleErrCode.DATABASE_ERROR: u'database error',

    # service error
    CreoleErrCode.VALIDATION_ERROR: u'validation error',
    CreoleErrCode.PARAMETER_ERROR: u'parameter error',

    # client error
    CreoleErrCode.USER_NAME_DUPLICATED: u'user name duplicated',
    CreoleErrCode.USER_NOT_EXIST: u'user not exist',

    CreoleErrCode.COUNTRY_NAME_DUPLICATED: u'country name or name_en duplicated',
    CreoleErrCode.CITY_NAME_DUPLICATED: u'city name or name_en duplicated',
    CreoleErrCode.COUNTRY_NOT_EXIST: u'country do not exist',
    CreoleErrCode.CITY_NOT_EXIST: u'city do not exist',

    CreoleErrCode.SHOP_NOT_EXIST: u'shop do not exist',
    CreoleErrCode.SHOP_COMPANY_DUPLICATED: u'shop company name or name_en duplicated',
    CreoleErrCode.SHOP_COMPANY_NOT_EXIST: u'shop company do not exist',

    CreoleErrCode.VEHICLE_COMPANY_DUPLICATED: u'vehicle company name or name_en duplicated',
    CreoleErrCode.VEHICLE_COMPANY_NOT_EXIST: u'vehicle company do not exist',
    CreoleErrCode.VEHICLE_NOT_EXIST: u'vehicle do not exist',
    CreoleErrCode.VEHICLE_ACCOUNT_NOT_EXIST: u'vehicle account do not exist',

    CreoleErrCode.ATTRACTION_NOT_EXIST: u'attraction do not exist',

    CreoleErrCode.RESTAURANT_COMPANY_NOT_EXIST: u'restaurant company do not exist',
    CreoleErrCode.RESTAURANT_COMPANY_DUPLICATED: u'restaurant company name or name_en duplicated',
    CreoleErrCode.RESTAURANT_NOT_EXIST: u'restaurant do not exist',
    CreoleErrCode.RESTAURANT_MEAL_REACH_LIMIT: u'the meal type of the restaurant has reach the limit.',
    CreoleErrCode.RESTAURANT_MEAL_TYPE_NOT_EXIST: u'the type of the meal dose not exist',

    CreoleErrCode.TOUR_GUIDE_NOT_EXIST: u'the tour guide do not exist',
    CreoleErrCode.TOUR_GUIDE_ID_DUPLICATED: u'the tour guide id duplicated',
    CreoleErrCode.TOUR_GUIDE_ACCOUNT_DUPLICATED: u'the account of tour guide duplicated',
    CreoleErrCode.TOUR_GUIDE_ACCOUNT_NOT_EXIST: u'the account of the tour guide do not exist',
    CreoleErrCode.TOUR_GUIDE_FEE_NOT_EXIST: u'the tour guide fee do not exist',
}


def get_translation(code):
    return TRANSLATIONS.get(code, '')


class CreoleError(Exception):
    errcode = None
    msg_pat = None

    def __init__(self, errcode=None, msg=None, args=()):
        if not msg and (self.msg_pat and args):
            msg = self.msg_pat % args
        if not msg:
            msg = TRANSLATIONS.get(errcode, '') or None

        self.errcode = errcode or self.errcode
        self.msg = msg
        super(CreoleError, self).__init__(msg)

    def __str__(self):
        return unicode(self.msg)

    def __repr__(self):
        return u'{}({}, {})'.\
            format(self.__class__.__name__, self.errcode, self.msg).\
            encode('utf-8')


class SystemError(CreoleError):
    errcode = CreoleErrCode.UNKNOWN_SYSTEM_ERROR

    def __init__(self, errcode=None, msg=None, args=()):
        self.errcode = self.errcode
        self.msg = msg or TRANSLATIONS.get(self.errcode, '')
        super(SystemError, self).__init__(msg=self.msg)


class DatabaseError(CreoleError):
    errcode = CreoleErrCode.DATABASE_ERROR

    def __init__(self, errcode=None, msg=None, args=()):
        self.errcode = self.errcode
        self.msg = msg or TRANSLATIONS.get(self.errcode, '')
        super(DatabaseError, self).__init__(msg=self.msg)


class ClientError(CreoleError):
    pass


class InvalidateError(ClientError):
    msg_pat = 'invalidate argument: %r: %s'
    errcode = CreoleErrCode.VALIDATION_ERROR


class ParameterError(ClientError):
    msg_pat = 'parameter error: %r'
    errcode = CreoleErrCode.PARAMETER_ERROR
 

def raise_error_json(err_obj):
    assert isinstance(err_obj, CreoleError) is True
    raise err_obj
