import logging
import inspect

from flask import request
from flask_restful.reqparse import RequestParser, Argument
from werkzeug.exceptions import BadRequest

from ....exc import raise_error_json, ParameterError

logger = logging.getLogger(__name__)


class BaseRequestParser(RequestParser):

    def __init__(self, *args, **kwargs):
        super(BaseRequestParser, self).__init__(*args, **kwargs)
        self._add_customize_arguments()

    def _collect_customize_arguments(self):
        customize_arguments = []
        for value in self.__class__.__dict__.values():
            if isinstance(value, Argument):
                customize_arguments.append(value)
        return customize_arguments

    def _add_customize_arguments(self):
        for value in self.__class__.__dict__.values():
            if isinstance(value, Argument):
                self.add_argument(value)


class ApiMixinMeta(type):
    def __new__(cls, name, bases, attrs):
        cls = type.__new__(cls, name, bases, attrs)
        if name == 'ApiMixin':
            return cls
        _dict = attrs.get('meta', {})
        args_parser_dict = _dict.get('args_parser', None)
        if args_parser_dict is None:
            return cls

        def predicate(member):
            return (
                inspect.ismethod(member) and
                member.__name__ in ('put', 'get', 'post', 'delete')
            )

        def set_parser(parser_cls):
            def wrapper(func):
                def decorated(*args, **kwargs):
                    # method:url:values
                    logger.info(u'{}:{}:{} {} {}'.format(
                        request.method, request.url, request.values,
                        request.json, request.files
                    ))
                    try:
                        parsed_data = parser_cls().parse_args()
                    except BadRequest as e:
                        raise_error_json(ParameterError(msg=e.data['message']))
                    # method:url:validated_data
                    logger.info(u'{}:{}:{}'.format(
                        request.method, request.url, parsed_data
                    ))

                    # self
                    args[0].parsed_data = parsed_data
                    return func(*args, **kwargs)

                return decorated
            return wrapper

        for method_name, method in inspect.getmembers(cls, predicate):
            parser_cls = args_parser_dict.get(method_name, None) or \
                args_parser_dict.get('*', None)
            if parser_cls is not None:
                cls.method_name = set_parser(parser_cls)(method)


class ApiMixin:
    __meta__ = ApiMixinMeta
