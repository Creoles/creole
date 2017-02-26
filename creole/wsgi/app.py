import logging

from flask import Flask

from ..request import CreoleRequest
from ..log import setup_logging
from .api.v1 import blue_print as v1_bp


class CreoleApp(Flask):
    request_class = CreoleRequest

    def __init__(self, app_name):
        super(CreoleApp, self).__init__(app_name)
        self._register_blueprints()
        self._setup_logger()
        self._register_error_handlers()
        self._register_before_request_handlers()
        self._register_after_request_handlers()

    def _register_blueprints(self):
        """Register blueprints"""
        self.register_blueprint(v1_bp, url_prefix='/ota/api/v1')
        pass

    def _setup_logger(self):
        setup_logging(self.name)
        self.logger_name = self.name
        self._logger = logging.getLogger(self.name)

    def _register_error_handlers(self):
        pass

    def _register_before_request_handlers(self):
        pass

    def _register_after_request_handlers(self):
        pass


def wsgi_app(environ, start_response):
    """The application for gunicorn"""
    app = CreoleApp('creole')
    return app(environ, start_response)
