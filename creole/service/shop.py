# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError

from ..model import DBSession
from ..model.shop import Shop, ShopCompany
from .base import BaseService
from ..exc import (
    raise_error_json,
    DatabaseError,
)


class ShopService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        shop = Shop.get_by_id(id)
        return cls._get_db_obj_data_dict(shop)

    @classmethod
    def create_shop(cls, name, name_en, address, telephone, country_id,
                    city_id, company_id, shop_type, contact, fee_person,
                    commission_ratio, intro_cn='', intro_en=''):
        return Shop.create(
            name=name, name_en=name_en, address=address,
            telephone=telephone, country_id=country_id,
            city_id=city_id, company_id=company_id, shop_type=shop_type,
            contact=contact, fee_person=fee_person, intro_cn=intro_cn,
            intro_en=intro_en, commission_ratio=commission_ratio)

    @classmethod
    def delete_shop_by_id(cls, id):
        return Shop.delete(id)

    @classmethod
    def update_shop_by_id(cls, id, **kwargs):
        return Shop.update(id, **kwargs)

    @classmethod
    def search_shop(cls, country_id=None, city_id=None,
                    company_id=None, shop_type=None, page=1, number=20):
        raw_data = []
        shop_list, total = Shop.search(
            country_id=country_id, city_id=city_id,
            company_id=company_id, shop_type=shop_type,
            page=page, number=number)
        for shop in shop_list:
            raw_data.append(cls._get_db_obj_data_dict(shop))
        return raw_data, total


class ShopCompanyService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        company_info = {}
        company = ShopCompany.get_by_id(id)
        shop_list = Shop.get_by_company_id(id)
        if not company:
            return company_info
        company_info['id'] = company.id
        company_info['name'] = company.name
        company_info['name_en'] = company.name_en
        company_info['shop_list'] = \
            [cls._get_db_obj_data_dict(item) for item in shop_list]
        return company_info

    @classmethod
    def delete_shop_company_by_id(cls, id):
        """删除商店公司, 有两个步骤:
        1. 删除公司
        2. 删除公司名下所有商店
        """
        session = DBSession()
        ShopCompany.delete(id)
        shop_list = Shop.get_by_company_id(id)
        for shop in shop_list:
            session.delete(shop)
        try:
            session.flush()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_shop_company_by_id(cls, id, **kwargs):
        return ShopCompany.update(id, **kwargs)

    @classmethod
    def create_shop_company(cls, name, name_en):
        return ShopCompany.create(name=name, name_en=name_en)

    @classmethod
    def search_company(cls, name=None, name_en=None, is_all=False):
        shop_company = \
            ShopCompany.search(name=name, name_en=name_en, is_all=is_all)
        return cls._get_db_obj_data_dict(shop_company)
