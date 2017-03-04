# coding: utf-8
import logging
import inspect

from flask import request
from flask_restful import Resource as BaseResource
from flask_restful.reqparse import RequestParser, Argument
from werkzeug.exceptions import BadRequest

from ...exc import raise_error_json, ParameterError

logger = logging.getLogger(__name__)

method_decorate_initialized = False


class BaseRequestParser(RequestParser):
    def __init__(self, *args, **kwargs):
        super(BaseRequestParser, self).__init__(*args, **kwargs)
        self._add_customize_arguments()

    def _add_customize_arguments(self):
        for value in self.__class__.__dict__.values():
            if isinstance(value, Argument):
                self.add_argument(value)


class Resource(BaseResource):
    def _set_req_method_decorate(self):
        self._req_method_decorate = {} 
        _dict = getattr(self, 'meta', {})
        args_parser_dict = _dict.get('args_parser_dict', None)
        if args_parser_dict is None:
            return self._req_method_decorate

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
                    return func(**kwargs)

                return decorated
            return wrapper

        for method_name, method in inspect.getmembers(self, predicate):
            parser_cls = args_parser_dict.get(method_name, None) or \
                args_parser_dict.get('*', None)
            if parser_cls is not None:
                self._req_method_decorate[method_name] = [set_parser(parser_cls)]

    def _set_method_decorate(self):
        global method_decorate_initialized 
        if not method_decorate_initialized:
            # flask-restulf==0.3.5目前还不支持针对不同的request method
            # 加不同的decorate, 需要使用比较tricky的方法
            # self.method_decorators = self._set_req_method_decorate()
            for meth_name in ('post', 'put', 'get', 'delete'):
                meth = getattr(self, meth_name, None)
                if meth:
                    self._set_req_method_decorate()
                    setattr(self, meth_name, self._req_method_decorate[meth_name][0](meth))
            method_decorate_initialized = True
    
    def dispatch_request(self, *args, **kwargs):
        self._set_method_decorate()
        super(Resource, self).dispatch_request(self, *args, **kwargs)
