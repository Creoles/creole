# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError

from ..model import DBSession
from ..model.shop import Shop, ShopCompany, ShopCompanyContact
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
        company = ShopCompany.get_by_id(id)
        return cls._get_db_obj_data_dict(company)

    @classmethod
    def delete_shop_company_by_id(cls, id):
        """删除商店公司, 有三个步骤:
        1. 删除公司
        2. 删除公司名下所有商店
        3. 删除公司联系人
        """
        session = DBSession()
        ShopCompany.delete(id)
        ShopCompanyContact.delete_by_company_id(id)
        Shop.delete_by_company_id(id)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_shop_company_by_id(cls, id, **kwargs):
        ShopCompany.update(id, **kwargs)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create_shop_company(cls, country_id, city_id, name, name_en,
                            nickname_en, register_number, intro=None):
        ShopCompany.create(
            country_id=country_id, city_id=city_id, name=name,
            name_en=name_en, nickname_en=nickname_en,
            register_number=register_number, intro=intro
        )
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def search_company(cls, name=None, name_en=None, is_all=False):
        shop_company = \
            ShopCompany.search(name=name, name_en=name_en, is_all=is_all)
        return [cls._get_db_obj_data_dict(item) for item in shop_company]


class ShopCompanyContactService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        contact = ShopCompanyContact.get_by_id(id)
        return cls._get_db_obj_data_dict(contact)

    @classmethod
    def get_by_company_id(cls, company_id):
        contact_list = ShopCompanyContact.get_by_company_id(company_id)
        return [cls._get_db_obj_data_dict(item) for item in contact_list]

    @classmethod
    def create_contact(cls, contact, position, telephone,
                       email, company_id):
        session = DBSession()
        contact = ShopCompanyContact.create(
            contact=contact, position=position,
            telephone=telephone, email=email,
            company_id=company_id)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))
        return contact.id

    @classmethod
    def update_contact(cls, id, **kwargs):
        session = DBSession()
        ShopCompanyContact.update(id, **kwargs)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_contact(cls, id):
        session = DBSession()
        ShopCompanyContact.delete(id)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))
