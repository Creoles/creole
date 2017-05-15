# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

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
    ClientError,
    CreoleErrCode,
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
        except IntegrityError as e:
            session.rollback()
            raise_error_json(ClientError(errcode=CreoleErrCode.VEHICLE_COMPANY_DUPLICATED))
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def search_company(cls, name=None, name_en=None, country_id=None,
                       city_id=None, company_type=None, number=20, page=1):
        vehicle_company, total = \
            VehicleCompany.search(
                name=name, name_en=name_en, country_id=country_id,
                city_id=city_id, company_type=company_type,
                number=number, page=page)
        return [cls._get_db_obj_data_dict(item) for item in vehicle_company], total


class VehicleAccountService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        account = VehicleAccount.get_by_id(id)
        return cls._get_db_obj_data_dict(account)

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
            company_id=company_id, currency=currency,
            bank_name=bank_name, deposit_bank=deposit_bank,
            payee=payee, account=account,
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
    def get_by_id(cls, id):
        fee = VehicleFee.get_by_id(id)
        return cls._get_db_obj_data_dict(fee)

    @classmethod
    def get_by_company_id(cls, company_id):
        fee_list = VehicleFee.get_by_company_id(company_id)
        return [cls._get_db_obj_data_dict(item) for item in fee_list]

    @classmethod
    def create_fee(cls, vehicle_type_id, company_id,
                   unit_price, start_time, end_time,
                   confirm_person, attachment_hash):
        session = DBSession()
        VehicleFee.create(
            vehicle_type_id=vehicle_type_id,
            company_id=company_id, unit_price=unit_price,
            start_time=start_time, end_time=end_time,
            confirm_person=confirm_person,
            attachment_hash=attachment_hash)
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

    @classmethod
    def search_fee(cls, vehicle_type_id=None, company_id=None,
                   unit_price=None, start_time=None, end_time=None,
                   confirm_person=None, number=20, page=1):
        fee_list, total = VehicleFee.search(
            vehicle_type_id=vehicle_type_id, company_id=company_id,
            unit_price=unit_price, start_time=start_time, end_time=end_time,
            confirm_person=confirm_person, number=number, page=page)
        return [cls._get_db_obj_data_dict(item) for item in fee_list], total


class VehicleContactService(BaseService):
    @classmethod
    def get_contact_by_id(cls, id):
        contact = VehicleContact.get_by_id(id)
        return cls._get_db_obj_data_dict(contact)

    @classmethod
    def get_contact_list_by_company_id(cls, company_id):
        contact_list = VehicleContact.get_by_company_id(company_id)
        return [cls._get_db_obj_data_dict(item) for item in contact_list]

    @classmethod
    def create_contact(cls, contact, position, telephone,
                       email, company_id):
        session = DBSession()
        VehicleContact.create(
            contact=contact, position=position,
            telephone=telephone, email=email,
            company_id=company_id)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_contact(cls, id, **kwargs):
        session = DBSession()
        VehicleContact.update(id, **kwargs)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_contact(cls, id):
        session = DBSession()
        VehicleContact.delete(id)
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
        VehicleType.update(id, **kwargs)
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

    @classmethod
    def search_type(cls, vehicle_type=None, number=20, page=1):
        type_list, total = VehicleType.search(
            vehicle_type=vehicle_type, number=number, page=page)
        return [cls._get_db_obj_data_dict(item) for item in type_list], total


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
            vehicle_type_id=None , license=None,page=1, number=20):
        raw_data = []
        vehicle_list, total = Vehicle.search(
            country_id=country_id, city_id=city_id,
            company_id=company_id, vehicle_type_id=vehicle_type_id,
            license=license, page=page, number=number)
        for vehicle in vehicle_list:
            raw_data.append(cls._get_db_obj_data_dict(vehicle))
        return raw_data, total
