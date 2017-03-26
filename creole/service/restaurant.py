# coding: utf-8
from ..model.restaurant import RestaurantCompany


class RestaurantCompanyService(object):
    @classmethod
    def get_by_id(cls, id):
        company_info = {}
        company = RestaurantCompany.get_by_id(id)
        if not company:
            return company_info
        company_info['id'] = company.id
        company_info['name'] = company.name
        company_info['name_en'] = company.name_en
        return company_info

    @classmethod
    def delete_restaurant_company_by_id(cls, id):
        return RestaurantCompany.delete(id)

    @classmethod
    def update_restaurant_company_by_id(cls, id, **kwargs):
        return RestaurantCompany.update(id, **kwargs)

    @classmethod
    def create_restaurant_company(cls, name, name_en):
        return RestaurantCompany.create(name=name, name_en=name_en)
