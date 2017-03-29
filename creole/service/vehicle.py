# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError

from ..model import DBSession
from ..model.vehicle import (
    Vehicle,
    VehicleCompany,
    VehicleAccount,
)
from .base import BaseService
from ..exc import (
    raise_error_json,
    DatabaseError,
)


class VehicleService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        vehicle = Vehicle.get_by_id(id)
        return cls._get_db_obj_data_dict(vehicle)

    @classmethod
    def create_vehicle(cls, account_id, company_id, country_id,
                       city_id, vehicle_type, seat, start_use, license,
                       register_number, contact, telephone, unit_price):
        return Vehicle.create(
            company_id=company_id, country_id=country_id, city_id=city_id,
            vehicle_type=vehicle_type, seat=seat, start_use=start_use,
            license=license, register_number=register_number, contact=contact,
            telephone=telephone, unit_price=unit_price, account_id=account_id
        )

    @classmethod
    def delete_vehicle_by_id(cls, id):
        return Vehicle.delete(id)

    @classmethod
    def update_vehicle_by_id(cls, id, **kwargs):
        return Vehicle.update(id, **kwargs)

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
            raw_data.append(cls._get_db_obj_data_dict(vehicle))
        return raw_data, total


class VehicleCompanyService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        company_info = {}
        company = VehicleCompany.get_by_id(id)
        vehicle_list = Vehicle.get_by_company_id(id)
        if not company:
            return company_info
        company_info['id'] = company.id
        company_info['name'] = company.name
        company_info['name_en'] = company.name_en
        company_info['vehicle_list'] = \
            [cls._get_db_obj_data_dict(item) for item in vehicle_list]
        return company_info

    @classmethod
    def delete_vehicle_company_by_id(cls, id):
        session = DBSession()
        VehicleCompany.delete(id)
        vehicle_list = Vehicle.get_by_company_id(id)
        for vehicle in vehicle_list:
            session.delete(vehicle)
        try:
            session.flush()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

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
        for k in account.__table__.columns._data:
            _dict[k] = getattr(account, k, None)
        return _dict

    @classmethod
    def create_account(cls, owner_id, account_type, currency, bank_name,
                       deposit_bank, payee, account, note=None):
        return VehicleAccount.create(
            owner_id=owner_id, currency=currency, bank_name=bank_name,
            deposit_bank=deposit_bank, payee=payee, account=account,
            note=note, account_type=account_type)

    @classmethod
    def get_by_owner_id(cls, owner_id):
        raw_data = []
        account_list = VehicleAccount.get_by_owner_id(owner_id)
        for account in account_list:
            raw_data.append(cls._get_account_data_dict(account))
        return raw_data

    @classmethod
    def delete_account_by_id(cls, id):
        return VehicleAccount.delete(id)

    @classmethod
    def update_account_by_id(cls, id, **kwargs):
        return VehicleAccount.update(id, **kwargs)
