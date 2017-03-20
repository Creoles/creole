# coding: utf-8
from ..model.vehicle import (
    Vehicle,
    VehicleCompany,
    VehicleUserAccount,
    VehicleCompanyAccount,
)


class VehicleService(object):
    @classmethod
    def get_by_id(cls, id):
        vehicle_info = {}
        vehicle = Vehicle.get_by_id(id)
        if not vehicle:
            return vehicle_info
        for k, v in vehicle.__dict__.iteritems():
            if not k.startswith('_'):
                vehicle_info[k] = v
        return vehicle_info

    @classmethod
    def create_vehicle(cls, company_id, country_id, city_id, vehicle_type,
               seat, start_use, license, register_number, contact,
               telephone, unit_price):
        return Vehicle.create(
            company_id=company_id, country_id=country_id, city_id=city_id,
            vehicle_type=vehicle_type, seat=seat, start_use=start_use,
            license=license, register_number=register_number, contact=contact,
            telephone=telephone, unit_price=unit_price)

    @classmethod
    def delete_vehicle_by_id(cls, id):
        return Vehicle.delete(id)

    @classmethod
    def update_vehicle_by_id(cls, id, **kwargs):
        return Vehicle.update(id, **kwargs)

    @classmethod
    def _get_vehicle_data_dict(cls, vehicle_obj):
        _vehicle_dict = {}
        for k, v in vehicle_obj.__dict__.iteritems():
            if not k.startswith('_'):
                _vehicle_dict[k] = v
        return _vehicle_dict

    @classmethod
    def search_vehicle(
            cls, country_id=None, city_id=None, company_id=None,
            vehicle_type=None, operation=None, seat=None, page=1, number=20):
        raw_data = []
        vehicle_list, total = Vehicle.search(
            country_id=country_id, city_id=city_id,
            company_id=company_id, vehicle_type=vehicle_type,
            operation=operation, seat=seat, page=page, number=number)
        for vehicle in vehicle_list:
            raw_data.append(cls._get_vehicle_data_dict(vehicle))
        return raw_data, total


class VehicleCompanyService(object):
    @classmethod
    def get_by_id(cls, id):
        company_info = {}
        company = VehicleCompany.get_by_id(id)
        if not company:
            return company_info
        company_info['id'] = company.id
        company_info['name'] = company.name
        company_info['name_en'] = company.name_en
        return company_info

    @classmethod
    def delete_vehicle_company_by_id(cls, id):
        return VehicleCompany.delete(id)

    @classmethod
    def update_vehicle_company_by_id(cls, id, **kwargs):
        return VehicleCompany.update(id, **kwargs)

    @classmethod
    def create_vehicle_company(cls, name, name_en):
        return VehicleCompany.create(name=name, name_en=name_en)


class VehicleAccountService(object):
    @classmethod
    def _get_account_data_dict(cls, account):
        _dict = {}
        for k ,v in account.__table__.columns._data.iteritems():
            _dict[k] = v
        return _dict

    @classmethod
    def create_user_account(cls, user_id, currency, bank_name, deposit_bank,
                            payee, account, note=None):
        return VehicleUserAccount.create(
            user_id=user_id, currency=currency, bank_name=bank_name,
            deposit_bank=deposit_bank, payee=payee, account=account,
            note=note)

    @classmethod
    def create_company_account(cls, company_id, currency, bank_name,
                               deposit_bank, payee, account, note=None):
        return VehicleCompanyAccount.create(
            company_id=company_id, currency=currency, bank_name=bank_name,
            deposit_bank=deposit_bank, payee=payee, account=account,
            note=note)

    @classmethod
    def get_by_user_id(cls, user_id):
        raw_data = []
        account_list = VehicleUserAccount.get_by_user_id(user_id)
        for account in account_list:
            raw_data.append(cls._get_account_data_dict(account))
        return raw_data

    @classmethod
    def get_by_company_id(cls, company_id):
        raw_data = []
        account_list = VehicleUserAccount.get_by_company_id(company_id)
        for account in account_list:
            raw_data.append(cls._get_account_data_dict(account))
        return raw_data

    @classmethod
    def delete_user_account_by_id(cls, id):
        return VehicleUserAccount.delete(id)

    @classmethod
    def delete_company_account_by_id(cls, id):
        return VehicleCompanyAccount.delete(id)

    @classmethod
    def update_user_account_by_id(cls, id, **kwargs):
        return VehicleUserAccount.update(id, **kwargs)

    @classmethod
    def update_company_account_by_id(cls, id, **kwargs):
        return VehicleCompanyAccount.update(id, **kwargs)
