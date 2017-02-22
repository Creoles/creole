# coding: utf-8
from flask import jsonify


class BaseCreoleErrCode(object):
    """Some general error code."""
    # unknown error
    UNKNOWN_SYSTEM_ERROR = 1001

    # database error
    DATABASE_ERROR = 1101

    # service error
    VALIDATION_ERROR = 2001
    PARAMETER_ERROR = 2002


class CreoleErrCode(BaseCreoleErrCode):
    pass


TRANSLATIONS = {
    200: u'ok',
    CreoleErrCode.UNKNOWN_SYSTEM_ERROR: u'unknown system error',

    CreoleErrCode.DATABASE_ERROR: u'database error',

    CreoleErrCode.VALIDATION_ERROR: u'validation error',
    CreoleErrCode.PARAMETER_ERROR: u'parameter error',
}


class CreoleError(Exception):
    errcode = None
    msg_pat = None

    def __init__(self, errcode=None, msg=None, args=()):
        if not msg and (self.msg_pat and args):
            msg = self.msg_pat % args

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

    def __init__(self):
        self.errcode = self.errcode
        self.msg = TRANSLATIONS.get(self.errcode, '')
        super(SystemError, self).__init__(self.msg)


class DatabaseError(CreoleError):
    errcode = CreoleErrCode.DATABASE_ERROR

    def __init__(self):
        self.errcode = self.errcode
        self.msg = TRANSLATIONS.get(self.errcode, '')
        super(SystemError, self).__init__(self.msg)


class InvalidateError(CreoleError):
    msg_pat = 'invalidate argument: %r: %s'
    errcode = CreoleErrCode.VALIDATION_ERROR


class ParameterError(CreoleError):
    msg_pat = 'parameter error: %r'
    errcode = CreoleErrCode.PARAMETER_ERROR


class ClientError(CreoleError):
    pass


def raise_error_json(err_obj):
    assert isinstance(err_obj, CreoleError)
    return jsonify({
        'result': err_obj.errcode,
        'message': err_obj.msg
    })
