# coding: utf-8
from ..service.user import AdminUserService, CustomerUserService

     
def create_user(user_name, password, role, customer_name=None,
                address=None, telephone=None, is_admin=False):
    """创建用户"""
    # TODO 权限问题
    if is_admin:
        return AdminUserService.create_user(user_name, password)
    return CustomerUserService.create_user(
        user_name, password, customer_name, address, telephone)
