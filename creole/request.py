import uuid

import flask

from .util import cached_property


class CreoleRequest(flask.Request):
    @cached_property
    def rid(self):
        return uuid.uuid4().hex

    @property
    def platform(self):
        return self.user_agent.platform

    @property
    def version(self):
        return self.user_agent.version or ''

    @property
    def ip_route_list(self):
        ip_list = list(self.access_route)
        if self.remote_addr and ip_list \
                and ip_list[-1] != self.remote_addr:
            ip_list.append(self.remote_addr)
        return ip_list
