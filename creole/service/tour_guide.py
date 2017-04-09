# coding: utf-8
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from ..model import DBSession
from ..model.tour_guide import (
    TourGuide,
    TourGuideFee,
    TourGuideAccount,
)
from .base import BaseService
from ..exc import (
    raise_error_json,
    DatabaseError,
    ClientError,
    CreoleErrCode,
    InvalidateError,
)


class TourGuideService(BaseService):
    @classmethod
    def get_by_id(cls, id):
        tour_guide = TourGuide.get_by_id(id)
        return cls._get_db_obj_data_dict(tour_guide)

    @classmethod
    def create_tour_guide(cls, guide_type, country_id, name, name_en, gender, birthday,
                          start_work, language, certificate_type, certificate_number,
                          tour_guide_numer, telephone, image_hash,
                          passport_country=None, intro=None):
        session = DBSession()
        TourGuide.create(
            guide_type=guide_type, country_id=country_id, name=name,
            name_en=name_en, gender=gender, birthday=birthday,
            start_work=start_work, language=language,
            certificate_type=certificate_type, certificate_number=certificate_number,
            tour_guide_numer=tour_guide_numer, passport_country=passport_country,
            telephone=telephone, intro=intro, image_hash=image_hash)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_tour_guide_by_id(cls, id, **kwargs):
        session = DBSession()
        TourGuide.update(id, **kwargs)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_tour_guide_by_id(cls, id):
        """删除导游有三个步骤:
        1. 删除导游基本资料
        2. 删除导游的费率信息
        3. 删除导游的银行账户资料
        """
        session = DBSession()
        TourGuide.delete(id)  # 删除基本资料
        TourGuideFee.delete(tour_guide_id=id)  # 删除费率信息
        TourGuideAccount.delete(tour_guide_id=id)  # 删除银行账户资料
        try:
            session.flush()
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class TourGuideFeeService(BaseService):
    @classmethod
    def get_by_tour_guide_id(cls, tour_guide_id):
        fee = TourGuideFee.get_by_tour_guide_id(tour_guide_id)
        return cls._get_db_obj_data_dict(fee)

    @classmethod
    def create_tour_guide_fee(cls, tour_guide_id, currency, base_fee,
                              service_type, service_fee):
        session = DBSession()
        TourGuideFee.create(
            tour_guide_id=tour_guide_id, currency=currency,
            base_fee=base_fee, service_type=service_type,
            service_fee=service_fee)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.TOUR_GUIDE_ID_DUPLICATED))
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def update_tour_guide_fee_by_id(cls, id, **kwargs):
        session = DBSession()
        TourGuideFee.update(id, **kwargs)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def delete_tour_guide_fee_by_id(cls, id):
        session = DBSession()
        TourGuideFee.delete(id=id)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))


class TourGuideAccountService(BaseService):
    @classmethod
    def get_by_tour_guide_id(cls, tour_guide_id):
        _list = []
        account_list = TourGuideAccount.get_by_tour_guide_id(tour_guide_id)
        for account in account_list:
            _list.append(cls._get_db_obj_data_dict(account))
        return _list

    @classmethod
    def edit_tour_guide_account(
            cls, create_list=None,
            update_list=None, delete_id_list=None):
        """编辑导游银行资料:
        
        :param create_list: 需要创建的银行资料列表, 元素为dict
        :param update_list: 需要更新的银行资料列表, 元素为dict
        :param delete_id_list: 需要删除的银行资料Id列表
        """
        session = DBSession()
        if create_list:
            cls.create_tour_guide_account(create_list)
        if update_list:
            cls.update_tour_guide_account(update_list)
        if delete_id_list:
            cls.delete_tour_guide_account(delete_id_list)
        try:
            session.commit()
        except IntegrityError as e:
            session.rollback()
            raise_error_json(
                ClientError(errcode=CreoleErrCode.TOUR_GUIDE_ACCOUNT_DUPLICATED))
        except SQLAlchemyError as e:
            session.rollback()
            raise_error_json(DatabaseError(msg=repr(e)))

    @classmethod
    def create_tour_guide_account(cls, account_list):
        for account_dict in account_list:
            tour_guide_id = account_dict['tour_guide_id']
            currency = account_dict['currency']
            bank_name = account_dict['bank_name']
            deposit_bank = account_dict['deposit_bank']
            payee = account_dict['payee']
            account = account_dict['account']
            note = account_dict.get('note', None)
            TourGuideAccount.create(
                tour_guide_id=tour_guide_id, currency=currency,
                bank_name=bank_name, deposit_bank=deposit_bank,
                payee=payee, account=account, note=note)

    @classmethod
    def update_tour_guide_account(cls, update_list):
        for account_dict in update_list:
            TourGuideAccount.update(**account_dict.__dict__)

    @classmethod
    def delete_tour_guide_account(cls, delete_id_list):
        for id in delete_id_list:
            TourGuideAccount.delete(id=id)
