from backend.app.extension.extensions import ext
from typing import Self
from backend.app.core.decorator.decorators import Decorators
from backend.app.core.const.enum import ENUM_FILTERS_USER, ENUM_FILTERS_TOKEN
from backend.app.exeptions.custom_exeptions import (
    FilterUserMissingError,
    FilterTokenMissingError,
)
from backend.app.models.models import Model_USER, Model_TOKEN_BLOCK_LIST


@Decorators.singleton
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

        return (
            Model_USER.filter_by(**filters).all()
            if multiple
            else Model_USER.filter_by(**filters).first()
        )

    def find_token_by_filters(self, multiple: bool = False, **kwargs: dict):
        filters: dict[str:...] = {
            key: value
            for key, value in kwargs.items()
            if key in ENUM_FILTERS_TOKEN.FILTERS.value
        }

        if not filters:
            raise FilterTokenMissingError(ENUM_FILTERS_TOKEN.FILTERS.value)

        return (
            Model_TOKEN_BLOCK_LIST.filter_by(**filters).all()
            if multiple
            else Model_TOKEN_BLOCK_LIST.filter_by(**filters).first()
        )

    def add_to_db(self, data) -> None:
        try:
            self._db.session.add(data)
            self.commit_to_db()
        except Exception as e:
            print(e)

    def commit_to_db(self) -> None:
        self._db.session.commit()


service_db: Service_DB = Service_DB()
