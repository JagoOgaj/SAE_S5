from backend.app.extension.extensions import ext
from typing import Self
from backend.app.core.const.enum import (
    ENUM_FILTERS_USER, 
    ENUM_FILTERS_TOKEN,
    ENUM_FIELDS_USER
)
from backend.app.exeptions.custom_exeptions import (
    FilterUserMissingError,
    FilterTokenMissingError,
    FieldsUserMissingError
)
from backend.app.models.models import Model_USER, Model_TOKEN_BLOCK_LIST
from sqlalchemy.exc import SQLAlchemyError


class Service_DB:
    def __init__(self: Self) -> None:
        self._db = ext.db_ext

    def find_user_by_filters(self, multiple: bool = False, **kwargs: dict):
        filters: dict[str:...] = {
            key: value
            for key, value in kwargs.items()
            if key in ENUM_FILTERS_USER.FILTERS.value
        }

        if not filters:
            raise FilterUserMissingError(ENUM_FILTERS_USER.FILTERS.value)
        
        query = Model_USER.filter_by(**filters)
        
        return (
            query.all()
            if multiple
            else query.first()
        )

    def create_user(self, data: dict[... : ...], userType) -> None:
        missing_fields = [field for field in ENUM_FIELDS_USER.FIELDS.value if field not in data.items()]
        
        if missing_fields:
            raise FieldsUserMissingError(ENUM_FIELDS_USER.FIELDS.value)
        
        newUser = Model_USER(
            _email = data[ENUM_FIELDS_USER.FIELDS.value[0]],
            _pseudo = data[ENUM_FIELDS_USER.FIELDS.value[1]],
            _password_hash=ext.pwd_context_ext.hash(data[ENUM_FIELDS_USER.FIELDS.value[2]]),
            _role_id = 1 if userType == 'admin' else 2
        )
        
        self.add_to_db(newUser)
        self.commit_to_db()
        
    def find_token_by_filters(self, multiple: bool = False, **kwargs: dict):
        filters: dict[str:...] = {
            key: value
            for key, value in kwargs.items()
            if key in ENUM_FILTERS_TOKEN.FILTERS.value
        }

        if not filters:
            raise FilterTokenMissingError(ENUM_FILTERS_TOKEN.FILTERS.value)

        query = Model_TOKEN_BLOCK_LIST.filter_by(**filters)
        
        return (
            query.all()
            if multiple
            else query.first()
        )
        
    def add_to_db(self, data) -> None:
        try:
            self._db.session.add(data)
        except (Exception, SQLAlchemyError) as e:
            self._db.session.rollback()
            raise Exception(str(e))

    def commit_to_db(self) -> None:
        self._db.session.commit()
    
    def delete_data(self, dataToDell) -> None:
        try:
            self._db.session.delete(dataToDell)
        except (Exception, SQLAlchemyError) as e:
            self._db.session.rollback()
            raise Exception(str(e))


            


service_db: Service_DB = Service_DB()
