# coding: utf-8
from ..model.shop import Shop, ShopCompany


class ShopService(object):
    @classmethod
    def get_by_id(cls, id):
        shop_info = {}
        shop = Shop.get_by_id(id)
        if not shop:
            return shop_info
        for k, v in shop.__dict__.iteritems():
            if not k.startswith('_'):
                shop_info[k] = v
        return shop_info

    @classmethod
    def create_shop(cls, name, name_en, address, telephone, country_id,
                    city_id, belong, shop_type, contact, fee_person,
                    commission_ratio, intro_cn='', intro_en=''):
        return Shop.create(
            name=name, name_en=name_en, address=address,
            telephone=telephone, country_id=country_id,
            city_id=city_id, belong=belong, shop_type=shop_type,
            contact=contact, fee_person=fee_person, intro_cn=intro_cn,
            intro_en=intro_en, commission_ratio=commission_ratio)

    @classmethod
    def delete_shop_by_id(cls, id):
        return Shop.delete(id)

    @classmethod
    def update_shop_by_id(cls, id, **kwargs):
        return Shop.update(id, **kwargs)

    @classmethod
    def _get_shop_data_dict(cls, shop_obj):
        _shop_dict = {}
        for k, v in shop_obj.__dict__.iteritems():
            if not k.startswith('_'):
                _shop_dict[k] = v
        return _shop_dict

    @classmethod
    def search_shop(cls, country_id=None, city_id=None,
                    company_id=None, shop_type=None, page=1, number=20):
        raw_data = []
        shop_list = Shop.search(
            country_id=country_id, city_id=city_id,
            company_id=company_id, shop_type=shop_type,
            page=page, number=number)
        for shop in shop_list:
            raw_data.append(cls._get_shop_data_dict(shop))
        return raw_data


class ShopCompanyService(object):
    @classmethod
    def get_by_id(cls, id):
        company_info = {}
        company = ShopCompany.get_by_id(id)
        if not company:
            return company_info
        company_info['id'] = company.id
        company_info['name'] = company.name
        company_info['name_en'] = company.name_en
        return company_info

    @classmethod
    def delete_shop_company_by_id(cls, id):
        return ShopCompany.delete(id)

    @classmethod
    def update_shop_company_by_id(cls, id, **kwargs):
        return ShopCompany.update(id, **kwargs)

    @classmethod
    def create_shop_company(cls, name, name_en):
        return ShopCompany.create(name=name, name_en=name_en)
