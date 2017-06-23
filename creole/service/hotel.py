# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError

from ..model import DBSession
from ..model.hotel import (
    HotelCompanyContact,
    HotelCompany,
    Hotel,
    HotelAccount,
    HotelContact,
    HotelFee,
    RoomPrice,
    MealPrice,
    RoomAdditionalCharge,
    FestivalAdditionalCharge,
)
from .base import BaseService
from ..exc import (
    raise_error_json,
    DatabaseError,
)
from ..util import timestamp_to_date, _func


class HotelCompanyContactService(BaseService):
    @classmethod
    def get_contact_by_id(cls, id):
        contact = HotelCompanyContact.get_by_id(id)
        return cls._get_db_obj_data_dict(contact)

    @classmethod
    def get_contact_list_by_company_id(cls, company_id):
        contact_list = HotelCompanyContact.get_by_company_id(company_id)
        return [cls._get_db_obj_data_dict(item) for item in contact_list]

    @classmethod
    def create_contact(cls, contact, position, telephone,
                       email, company_id):
        session = DBSession()
        contact = HotelCompanyContact.create(
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
        HotelCompanyContact.update(id, **kwargs)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_contact(cls, id):
        session = DBSession()
        HotelCompanyContact.delete(id)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class HotelCompanyService(BaseService):
    @classmethod
    def get_by_id(cls, company_id):
        company = HotelCompany.get_by_id(company_id)
        return cls._get_db_obj_data_dict(company)

    @classmethod
    def create_hotel_company(cls, country_id, city_id, name, name_en,
                             nickname_en, register_number, intro=None,
                             note=None):
        HotelCompany.create(
            country_id=country_id, city_id=city_id,
            name=name, name_en=name_en, nickname_en=nickname_en,
            register_number=register_number,
            intro=intro, note=note
        )
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_hotel_company(cls, id, **kwargs):
        HotelCompany.update(id, **kwargs)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_hotel_company(cls, id):
        """删除酒店公司, 有以下几步:
        
        1. 删除公司
        2. 删除公司联系人
        3. 删除公司下所有酒店
        4. 删除公司对应酒店的所有联系人
        5. 删除公司对应酒店的所有费率
        6. 删除公司对应酒店的所有账户
        """
        hotel_id_list = Hotel.get_by_company_id(id)
        for hotel_id in hotel_id_list:
            # 删除所有费率信息
            fee_id = HotelFee.get_by_hotel_id(hotel_id)
            HotelFee.delete(fee_id)
            RoomPrice.delete_by_hotel_fee_id(fee_id)
            MealPrice.delete_by_hotel_fee_id(fee_id)
            RoomAdditionalCharge.delete_by_hotel_fee_id(fee_id)
            FestivalAdditionalCharge.delete_by_hotel_fee_id(fee_id)

            # 删除所有酒店联系人
            HotelContact.delete_by_hotel_id(hotel_id)

            # 删除所有酒店账户
            HotelAccount.delete_by_hotel_id(hotel_id)

        # 删除酒店
        Hotel.delete_by_company_id(id)

        # 删除公司联系人
        HotelCompanyContact.delete_by_company_id(id)

        # 删除公司
        HotelCompany.delete(id)

        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def search_hotel_company(cls, country_id=None, city_id=None,
                             page=1, number=20):
        company_list, total = \
            HotelCompany.search(
                country_id=country_id, city_id=city_id,
                page=page, number=number
            )
        return [cls._get_db_obj_data_dict(item) for item in company_list], total


class HotelService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        hotel = Hotel.get_by_id(id)
        return cls._get_db_obj_data_dict(hotel)

    @classmethod
    def get_by_company_id(cls, company_id):
        hotel = Hotel.get_by_company_id(company_id)
        return cls._get_db_obj_data_dict(hotel)

    @classmethod
    def create_hotel(cls, country_id, city_id, company_id, address, name,
                     name_en, nickname_en, star_level, comment_level,
                     standard_room_number, standard_double_room_number,
                     triple_room_number, suite_room_number, tour_guide_room_number,
                     start_year, telephone, email, intro_cn=None, intro_en=None):
        Hotel.create(
            country_id=country_id, city_id=city_id, company_id=company_id,
            address=address, name=name, name_en=name_en, nickname_en=nickname_en,
            star_level=star_level, comment_level=comment_level,
            standard_room_number=standard_room_number,
            standard_double_room_number=standard_double_room_number,
            triple_room_number=triple_room_number,
            suite_room_number=suite_room_number,
            tour_guide_room_number=tour_guide_room_number,
            start_year=start_year, telephone=telephone, email=email,
            intro_cn=intro_cn, intro_en=intro_en
        )
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_hotel(cls, id, **kwargs):
        Hotel.update(id, **kwargs)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_hotel(cls, id):
        """删除酒店, 有以下几个步骤:
            
        1. 删除酒店
        2. 删除酒店费率信息
        3. 删除酒店联系人
        4. 删除酒店账户信息
        """
        # 删除酒店费率信息
        fee_id = HotelFee.get_by_hotel_id(id)
        HotelFee.delete(fee_id)
        RoomPrice.delete_by_hotel_fee_id(fee_id)
        MealPrice.delete_by_hotel_fee_id(fee_id)
        RoomAdditionalCharge.delete_by_hotel_fee_id(fee_id)
        FestivalAdditionalCharge.delete_by_hotel_fee_id(fee_id)

        # 删除所有酒店联系人
        HotelContact.delete_by_hotel_id(id)

        # 删除所有酒店账户
        HotelAccount.delete_by_hotel_id(id)

        # 删除酒店
        Hotel.delete(id)

        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def search_hotel(cls, country_id=None, city_id=None, company_id=None,
                     name=None, name_en=None, nickname_en=None,
                     star_level=None, page=1, number=20):
        raw_data = []
        hotel_list, total = Hotel.search(
            country_id=country_id, city_id=city_id,
            company_id=company_id, name=name, name_en=name_en,
            nickname_en=nickname_en, star_level=star_level,
            page=page, number=number
        )
        for hotel in hotel_list:
            raw_data.append(cls._get_db_obj_data_dict(hotel))
        return raw_data, total 


class HotelAccountService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        account = HotelAccount.get_by_id(id)
        return cls._get_db_obj_data_dict(account)

    @classmethod
    def get_by_hotel_id(cls, hotel_id):
        account_list = HotelAccount.get_by_hotel_id(hotel_id)
        return [cls._get_db_obj_data_dict(account) for account in account_list]

    @classmethod
    def create_account(cls, hotel_id, currency, bank_name,
                       deposit_bank, payee, account,
                       swift_code=None, note=None):
        account = HotelAccount.create(
            hotel_id=hotel_id, currency=currency,
            bank_name=bank_name, deposit_bank=deposit_bank,
            payee=payee, account=account, swift_code=swift_code,
            note=note)
        session = DBSession()
        try:
            session.commit()
            return account.id
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_account(cls, id, **kwargs):
        HotelAccount.update(id, **kwargs)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_account(cls, id):
        HotelAccount.delete(id)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class HotelContactService(BaseService):
    @classmethod
    def get_contact_by_id(cls, id):
        contact = HotelContact.get_by_id(id)
        return cls._get_db_obj_data_dict(contact)

    @classmethod
    def get_contact_list_by_hotel_id(cls, hotel_id):
        contact_list = HotelContact.get_by_hotel_id(hotel_id)
        return [cls._get_db_obj_data_dict(item) for item in contact_list]

    @classmethod
    def create_contact(cls, contact, position, telephone,
                       email, hotel_id):
        session = DBSession()
        contact = HotelContact.create(
            contact=contact, position=position,
            telephone=telephone, email=email,
            hotel_id=hotel_id)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))
        return contact.id

    @classmethod
    def update_contact(cls, id, **kwargs):
        session = DBSession()
        HotelContact.update(id, **kwargs)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_contact(cls, id):
        session = DBSession()
        HotelContact.delete(id)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class HotelFeeService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        fee = HotelFee.get_by_id(id)
        return cls._get_db_obj_data_dict(fee)

    @classmethod
    def get_by_hotel_id(cls, hotel_id):
        fee = HotelFee.get_by_hotel_id(hotel_id)
        return cls._get_db_obj_data_dict(fee)

    @classmethod
    def create_hotel_fee(cls, hotel_id, confirm_person, free_policy=None,
                         free=None, note=None, attachment_hash=None):
        fee_id = HotelFee.create(
            hotel_id=hotel_id, confirm_person=confirm_person,
            free_policy=free_policy, free=free, note=note,
            attachment_hash=attachment_hash
        )
        session = DBSession()
        try:
            session.commit()
            return fee_id
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_fee(cls, id, **kwargs):
        HotelFee.update(id, **kwargs)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_fee(cls, id):
        """删除酒店费率信息"""
        HotelFee.delete(id)
        RoomPrice.delete_by_hotel_fee_id(id)
        MealPrice.delete_by_hotel_fee_id(id)
        RoomAdditionalCharge.delete_by_hotel_fee_id(id)
        FestivalAdditionalCharge.delete_by_hotel_fee_id(id)
        session = DBSession()
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class RoomPriceService(BaseService):
    @classmethod
    def get_by_hotel_fee_id(cls, fee_id):
        fee_list = RoomPrice.get_by_hotel_fee_id(fee_id)
        return [cls._get_db_obj_data_dict(item) for item in fee_list]

    @classmethod
    def edit_room_service(cls, create_list=None, update_list=None,
                          delete_id_list=None):
        session = DBSession()
        if create_list:
            cls.create_room_price(filter(_func, create_list))
        if update_list:
            cls.update_room_price(filter(_func, update_list))
        if delete_id_list:
            cls.delete_room_price(delete_id_list)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create_room_price(cls, price_list):
        for price_dict in price_list:
            start_time_stamp = int(price_dict['start_time'])
            end_time_stamp = int(price_dict['end_time'])
            price_dict['start_time'] = timestamp_to_date(start_time_stamp)
            price_dict['end_time'] = timestamp_to_date(end_time_stamp)
            RoomPrice.create(**price_dict)

    @classmethod
    def update_room_price(cls, price_list):
        for price_dict in price_list:
            start_time_stamp = int(price_dict['start_time'])
            end_time_stamp = int(price_dict['end_time'])
            price_dict['start_time'] = timestamp_to_date(start_time_stamp)
            price_dict['end_time'] = timestamp_to_date(end_time_stamp)
            RoomPrice.update(**price_dict)

    @classmethod
    def delete_room_price(cls, delete_id_list):
        for id in delete_id_list:
            RoomPrice.delete(id)


class MealPriceService(BaseService):
    @classmethod
    def get_by_hotel_fee_id(cls, fee_id):
        fee_list = MealPrice.get_by_hotel_fee_id(fee_id)
        return [cls._get_db_obj_data_dict(item) for item in fee_list]

    @classmethod
    def edit_meal_service(cls, create_list=None, update_list=None,
                          delete_id_list=None):
        session = DBSession()
        if create_list:
            cls.create_meal_price(filter(_func, create_list))
        if update_list:
            cls.update_meal_price(filter(_func, update_list))
        if delete_id_list:
            cls.delete_meal_price(delete_id_list)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create_meal_price(cls, price_list):
        for price_dict in price_list:
            start_time_stamp = int(price_dict['start_time'])
            end_time_stamp = int(price_dict['end_time'])
            price_dict['start_time'] = timestamp_to_date(start_time_stamp)
            price_dict['end_time'] = timestamp_to_date(end_time_stamp)
            MealPrice.create(**price_dict)

    @classmethod
    def update_meal_price(cls, price_list):
        for price_dict in price_list:
            start_time_stamp = int(price_dict['start_time'])
            end_time_stamp = int(price_dict['end_time'])
            price_dict['start_time'] = timestamp_to_date(start_time_stamp)
            price_dict['end_time'] = timestamp_to_date(end_time_stamp)
            MealPrice.update(**price_dict)

    @classmethod
    def delete_meal_price(cls, delete_id_list):
        for id in delete_id_list:
            MealPrice.delete(id)


class RoomAdditionalChargeService(BaseService):
    @classmethod
    def get_by_hotel_fee_id(cls, fee_id):
        fee_list = RoomAdditionalCharge.get_by_hotel_fee_id(fee_id)
        return [cls._get_db_obj_data_dict(item) for item in fee_list]

    @classmethod
    def edit_additional_charge_service(
            cls, create_list=None, update_list=None,
            delete_id_list=None):
        session = DBSession()
        if create_list:
            cls.create_additional_charge_price(filter(_func, create_list))
        if update_list:
            cls.update_additional_charge_price(filter(_func, update_list))
        if delete_id_list:
            cls.delete_additional_charge_price(delete_id_list)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create_additional_charge_price(cls, price_list):
        for price_dict in price_list:
            start_time_stamp = int(price_dict['start_time'])
            end_time_stamp = int(price_dict['end_time'])
            price_dict['start_time'] = timestamp_to_date(start_time_stamp)
            price_dict['end_time'] = timestamp_to_date(end_time_stamp)
            RoomAdditionalCharge.create(**price_dict)

    @classmethod
    def update_additional_charge_price(cls, price_list):
        for price_dict in price_list:
            start_time_stamp = int(price_dict['start_time'])
            end_time_stamp = int(price_dict['end_time'])
            price_dict['start_time'] = timestamp_to_date(start_time_stamp)
            price_dict['end_time'] = timestamp_to_date(end_time_stamp)
            RoomAdditionalCharge.update(**price_dict)

    @classmethod
    def delete_additional_charge_price(cls, delete_id_list):
        for id in delete_id_list:
            RoomAdditionalCharge.delete(id)


class FestivalAdditionalChargeService(BaseService):
    @classmethod
    def get_by_hotel_fee_id(cls, fee_id):
        fee_list = FestivalAdditionalCharge.get_by_hotel_fee_id(fee_id)
        return [cls._get_db_obj_data_dict(item) for item in fee_list]

    @classmethod
    def edit_additional_charge_service(
            cls, create_list=None, update_list=None,
            delete_id_list=None):
        session = DBSession()
        if create_list:
            cls.create_additional_charge_price(filter(_func, create_list))
        if update_list:
            cls.update_additional_charge_price(filter(_func, update_list))
        if delete_id_list:
            cls.delete_additional_charge_price(delete_id_list)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create_additional_charge_price(cls, price_list):
        for price_dict in price_list:
            start_time_stamp = int(price_dict['start_time'])
            end_time_stamp = int(price_dict['end_time'])
            price_dict['start_time'] = timestamp_to_date(start_time_stamp)
            price_dict['end_time'] = timestamp_to_date(end_time_stamp)
            FestivalAdditionalCharge.create(**price_dict)

    @classmethod
    def update_additional_charge_price(cls, price_list):
        for price_dict in price_list:
            start_time_stamp = int(price_dict['start_time'])
            end_time_stamp = int(price_dict['end_time'])
            price_dict['start_time'] = timestamp_to_date(start_time_stamp)
            price_dict['end_time'] = timestamp_to_date(end_time_stamp)
            FestivalAdditionalCharge.update(**price_dict)

    @classmethod
    def delete_additional_charge_price(cls, delete_id_list):
        for id in delete_id_list:
            FestivalAdditionalCharge.delete(id)
