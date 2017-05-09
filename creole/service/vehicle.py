# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError

from ..model import DBSession
from ..model.vehicle import (
    Vehicle,
    VehicleCompany,
    VehicleAccount,
    VehicleContact,
    VehicleFee,
    VehicleType,
)
from .base import BaseService
from ..exc import (
    raise_error_json,
    DatabaseError,
)


class VehicleCompanyService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        company = VehicleCompany.get_by_id(id)
        return cls._get_db_obj_data_dict(company)

    @classmethod
    def delete_vehicle_company_by_id(cls, id):
        """删除车辆公司, 有五个步骤:
        1. 删除公司
        2. 删除公司名下所有车辆
        3. 删除公司的结算账号
        4. 删除公司的费率信息
        5. 删除公司的联系人
        """
        session = DBSession()
        VehicleCompany.delete(id)   # 删除公司
        vehicle_list = Vehicle.get_by_company_id(id)
        # 删除公司下的车辆
        for vehicle in vehicle_list:
            session.delete(vehicle)
        # 删除公司结算账号
        account_list = VehicleAccount.get_by_company_id(id)
        for account in account_list:
            session.delete(account)
        # 删除公司费率信息
        fee_list = VehicleFee.get_by_company_id(id)
        for fee in fee_list:
            session.delete(fee)
        # 删除联系人
        contact_list = VehicleContact.get_by_company_id(id)
        for contact in contact_list:
            session.delete(contact)
        try:
            session.flush()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_vehicle_company_by_id(cls, id, **kwargs):
        VehicleCompany.update(id, **kwargs)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create_vehicle_company(cls, company_type, country_id, city_id,
                               name, name_en, nickname_en, vehicle_number,
                               register_number):
        VehicleCompany.create(
            company_type=company_type, country_id=country_id, city_id=city_id,
            name=name, name_en=name_en, nickname_en=nickname_en,
            vehicle_number=vehicle_number, register_number=register_number)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def search_company(cls, name=None, name_en=None, is_all=False):
        vehicle_company = \
            VehicleCompany.search(name=name, name_en=name_en, is_all=is_all)
        return [cls._get_db_obj_data_dict(item) for item in vehicle_company]


class VehicleAccountService(BaseService):
    @classmethod
    def get_by_company_id(cls, company_id):
        raw_data = []
        account_list = VehicleAccount.get_by_company_id(company_id)
        for account in account_list:
            raw_data.append(cls._get_db_obj_data_dict(account))
        return raw_data

    @classmethod
    def create_account(cls, company_id, currency, bank_name,
                       deposit_bank, payee, account, swift_code=None,
                       note=None):
        VehicleAccount.create(
            currency=currency, bank_name=bank_name,
            deposit_bank=deposit_bank, payee=payee, account=account,
            note=note, swift_code=swift_code)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_account_by_id(cls, id):
        VehicleAccount.delete(id)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_account_by_id(cls, id, **kwargs):
        VehicleAccount.update(id, **kwargs)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class VehicleFeeService(BaseService):
    @classmethod
    def create_fee(cls, vehicle_type_id, company_id,
                   unit_price, start_time, end_time,
                   confirm_id, attachment_hash):
        session = DBSession()
        VehicleFee.create(
            vehicle_type_id=vehicle_type_id,
            company_id=company_id, unit_price=unit_price,
            start_time=start_time, end_time=end_time,
            confirm_id=confirm_id, attachment_hash=attachment_hash)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_fee_by_id(cls, id, **kwargs):
        session = DBSession()
        VehicleFee.update(id, **kwargs)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_fee_by_id(cls, id):
        session = DBSession()
        VehicleFee.delete(id)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class VehicleContactService(BaseService):
    @classmethod
    def create_contact(cls, create_list):
        for contact_dict in create_list:
            contact = contact_dict['contact']
            position = contact_dict['position']
            telephone = contact_dict['telephone']
            email = contact_dict['email']
            company_id = contact_dict['company_id']
            VehicleContact.create(
                contact=contact, position=position,
                telephone=telephone, email=email,
                company_id=company_id)

    @classmethod
    def update_contact(cls, update_list):
        for item in update_list:
            VehicleContact.update(**item)

    @classmethod
    def delete_contact(cls, delete_id_list):
        for id in delete_id_list:
            VehicleContact.delete(id)

    @classmethod
    def edit_contact(cls, create_list=None, update_list=None,
                     delete_id_list=None):
        session = DBSession()
        if create_list:
            cls.create_contact(create_list)
        if update_list:
            cls.update_contact(update_list)
        if delete_id_list:
            cls.delete_contact(delete_id_list)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class VehicleTypeService(BaseService):
    @classmethod
    def get_type_by_id(cls, id):
        type = VehicleType.get_by_id(id)
        return cls._get_db_obj_data_dict(type)

    @classmethod
    def create_type(cls, vehicle_type, brand, seat,
                    available_seat, passenger_count, note=None):
        VehicleType.create(
            vehicle_type=vehicle_type, brand=brand, seat=seat,
            available_seat=available_seat, note=note,
            passenger_count=passenger_count)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_type_by_id(cls, id, **kwargs):
        VehicleType.updated(id, **kwargs)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_type_by_id(cls, id):
        VehicleType.delete(id)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class VehicleService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        vehicle = Vehicle.get_by_id(id)
        return cls._get_db_obj_data_dict(vehicle)

    @classmethod
    def create_vehicle(cls, country_id, city_id, company_id, license,
                       insurance_number, start_use, register_number,
                       vehicle_type_id):
        Vehicle.create(
            country_id=country_id, city_id=city_id, license=license,
            company_id=company_id, insurance_number=insurance_number,
            start_use=start_use, register_number=register_number,
            vehicle_type_id=vehicle_type_id
        )
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_vehicle_by_id(cls, id):
        Vehicle.delete(id)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_vehicle_by_id(cls, id, **kwargs):
        Vehicle.update(id, **kwargs)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def search_vehicle(
            cls, country_id=None, city_id=None, company_id=None,
            vehicle_type_id=None ,page=1, number=20):
        raw_data = []
        vehicle_list, total = Vehicle.search(
            country_id=country_id, city_id=city_id,
            company_id=company_id, vehicle_type_id=vehicle_type_id,
            page=page, number=number)
        for vehicle in vehicle_list:
            raw_data.append(cls._get_db_obj_data_dict(vehicle))
        return raw_data, total
