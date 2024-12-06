from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    TIMESTAMP,
    ForeignKey,
    TEXT,
    LargeBinary,
    CheckConstraint,
)
from core import (
    ENUM_COLUMN_TABLE_USER,
    ENUM_TABLE_DB,
    ENUM_MODEL_NAME,
    ENUM_ROLE,
    ENUM_COLUMN_TABLE_ROLE,
    ENUM_COLUMN_TABLE_CONVERSATION,
    ENUM_COLUMN_TABLE_CONVERSATION_IMAGES,
    ENUM_COLUMN_TABLE_CONVERSATION_MESSAGE,
    ENUM_ON_ACTION,
    ENUM_RELATIONSHIP,
    ENUM_FOREIGN_KEY,
    ENUM_MESSAGE_TYPE,
    ENUM_CONTRAINT,
    get_paris_time,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from extension import ext
from typing import Self


class Model_USER(ext.db_ext.Model):
    __tablename__ = ENUM_TABLE_DB.USER.value

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    _pseudo = Column(ENUM_COLUMN_TABLE_USER.NAME.value, String, nullable=False)
    _email = Column(ENUM_COLUMN_TABLE_USER.EMAIL.value, String, nullable=False)
    _password_hash = Column(
        ENUM_COLUMN_TABLE_USER.PWD_HASH.value, String, nullable=False
    )
    _role_id = Column(
        ENUM_COLUMN_TABLE_USER.ROLE_ID.value,
        Integer,
        ForeignKey(ENUM_FOREIGN_KEY.ROLE.value, ondelete=ENUM_ON_ACTION.SET_NULL.value),
        nullable=False,
    )

    role = relationship(
        ENUM_MODEL_NAME.ROLE.value, back_populates=ENUM_TABLE_DB.USER.value
    )
    conversation = relationship(
        ENUM_MODEL_NAME.CONVERSATION.value,
        back_populates=ENUM_TABLE_DB.CONVERSATION.value,
        cascade=ENUM_RELATIONSHIP.CASCADE.value,
    )

    @hybrid_property
    def pseudo(self: Self) -> str:
        return self._pseudo

    @pseudo.setter
    def pseudo(self: Self, value: str) -> None:
        self._pseudo = value

    @hybrid_property
    def email(self: Self) -> str:
        return self._email

    @email.setter
    def email(self: Self, value: str) -> None:
        self._email = value

    @hybrid_property
    def password_hash(self: Self) -> str:
        return self._password_hash

    @password_hash.setter
    def password_hash(self: Self, value: str) -> None:
        self._password_hash = ext.pwd_context_ext.hash(value)

    @hybrid_property
    def role_name(self: Self):
        return self.role.role_name if self.role else None

    @role_name.expression
    def role_name(cls: object) -> bool:
        return cls.role.has()

    @hybrid_property
    def is_admin(self: Self) -> bool:
        return self.role.role_name == ENUM_ROLE.ADMIN.value

    @is_admin.expression
    def is_admin(cls: object) -> bool:
        return cls.role.has(role_name=ENUM_ROLE.ADMIN.value)


class Model_ROLE(ext.db_ext.Model):
    __tablename__ = ENUM_TABLE_DB.ROLE.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    _name = Column(
        Enum(ENUM_ROLE, name=ENUM_COLUMN_TABLE_ROLE.NAME.value),
        nullable=False,
        unique=True,
    )

    @hybrid_property
    def role_name(self: Self) -> str:
        return self._name

    @role_name.setter
    def role_name(self: Self, value: str) -> None:
        self._name = value

    users = relationship(
        ENUM_MODEL_NAME.USER.value, back_populates=ENUM_TABLE_DB.ROLE.value
    )


class Model_CONVERSATION(ext.db_ext.Model):
    __tablename__ = ENUM_TABLE_DB.CONVERSATION.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    _user_id = Column(
        String,
        name=ENUM_COLUMN_TABLE_CONVERSATION.USER_ID.value,
        nullable=False,
        unique=True,
    )
    _name = Column(
        String,
        name=ENUM_COLUMN_TABLE_CONVERSATION.NAME.value,
        nullable=False,
        unique=False,
    )
    _start_date = Column(
        TIMESTAMP,
        name=ENUM_COLUMN_TABLE_CONVERSATION.START_DATE.value,
        default=get_paris_time,
    )

    user = relationship(
        ENUM_MODEL_NAME.USER.value, back_populates=ENUM_TABLE_DB.CONVERSATION.value
    )
    messages = relationship(
        ENUM_MODEL_NAME.CONVERSATION_MESSAGE.value,
        back_populates=ENUM_TABLE_DB.CONVERSATION.value,
        cascade=ENUM_RELATIONSHIP.CASCADE.value,
    )
    images = relationship(
        ENUM_MODEL_NAME.CONVERSATION_IMAGE.value,
        back_populates=ENUM_TABLE_DB.CONVERSATION.value,
        cascade=ENUM_RELATIONSHIP.CASCADE.value,
    )

    @hybrid_property
    def user_id(self: Self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self: Self, value: int) -> None:
        self._user_id = value

    @hybrid_property
    def name(self: Self) -> str:
        return self._name

    @name.setter
    def name(self: Self, value: str) -> None:
        self._name = value

    @hybrid_property
    def start_date(self: Self):
        return self._start_date

    @start_date.setter
    def start_date(self: Self, value) -> None:
        self._start_date = value


class Model_CONVERSATION_MESSAGE(ext.db_ext.Model):
    __tablename__ = ENUM_TABLE_DB.CONVERSATION_MESSAGES.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    _conversation_id = Column(
        Integer,
        ForeignKey(
            ENUM_FOREIGN_KEY.CONVERSATION.value, ondelete=ENUM_ON_ACTION.CASCADE.value
        ),
        name=ENUM_COLUMN_TABLE_CONVERSATION_MESSAGE.CONVERSATION_ID.value,
        nullable=False,
    )
    _message_type = Column(
        Enum(
            ENUM_MESSAGE_TYPE,
            name=ENUM_COLUMN_TABLE_CONVERSATION_MESSAGE.MESSAGE_TYPE.value,
        ),
        nullable=False,
    )
    _content = Column(
        TEXT, name=ENUM_COLUMN_TABLE_CONVERSATION_MESSAGE.CONTENT.value, nullable=False
    )
    _created_at = Column(
        TIMESTAMP,
        name=ENUM_COLUMN_TABLE_CONVERSATION_MESSAGE.CREATED_AT.value,
        default=get_paris_time,
    )

    conversation = relationship(
        ENUM_MODEL_NAME.CONVERSATION.value,
        back_populates=ENUM_TABLE_DB.CONVERSATION_MESSAGES.value,
    )

    @hybrid_property
    def conversation_id(self: Self) -> int:
        return self._conversation_id

    @conversation_id.setter
    def conversation_id(self: Self, value: int) -> None:
        self._conversation_id = value

    @hybrid_property
    def message_type(self: Self) -> str:
        return self._message_type

    @message_type.setter
    def message_type(self: Self, value: str) -> None:
        self._message_type = value

    @hybrid_property
    def content(self: Self) -> str:
        return self._content

    @content.setter
    def content(self: Self, value: str) -> None:
        self._content = value

    @hybrid_property
    def created_at(self: Self):
        return self._created_at

    @created_at.setter
    def created_at(self: Self, value) -> None:
        self._created_at = value


class Model_CONVERSATION_IMAGES(ext.db_ext.Model):
    __tablename__ = ENUM_TABLE_DB.CONVERSATION_IMAGES.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    _conversation_id = Column(
        Integer,
        ForeignKey(
            ENUM_FOREIGN_KEY.CONVERSATION.value, ondelete=ENUM_ON_ACTION.CASCADE.value
        ),
        name=ENUM_COLUMN_TABLE_CONVERSATION_MESSAGE.CONVERSATION_ID.value,
        nullable=False,
    )
    _image_data = Column(
        LargeBinary,
        name=ENUM_COLUMN_TABLE_CONVERSATION_IMAGES.IMAGE_DATA.value,
        nullable=False,
    )
    _image_size = Column(
        Integer,
        name=ENUM_COLUMN_TABLE_CONVERSATION_IMAGES.IMAGE_SIZE.value,
        nullable=False,
    )
    _created_at = Column(
        TIMESTAMP,
        name=ENUM_COLUMN_TABLE_CONVERSATION_IMAGES.CREATED_AT.value,
        default=get_paris_time,
    )

    conversation = relationship(
        ENUM_MODEL_NAME.CONVERSATION.value,
        back_populates=ENUM_TABLE_DB.CONVERSATION_IMAGES.value,
    )

    __table_args__ = (
        CheckConstraint(
            ENUM_CONTRAINT.CONVERSATION_IMAGES.value[0],
            name=ENUM_CONTRAINT.CONVERSATION_IMAGES.value[1],
        ),
    )

    @hybrid_property
    def conversation_id(self: Self) -> int:
        return self._conversation_id

    @conversation_id.setter
    def conversation_id(self: Self, value: int) -> None:
        self._conversation_id = value

    @hybrid_property
    def image_data(self: Self):
        return self._image_data

    @image_data.setter
    def image_data(self: Self, value: bytes) -> None:
        self._image_data = value

    @hybrid_property
    def image_size(self: Self) -> int:
        return self._image_size

    @image_size.setter
    def image_size(self: Self, value: int) -> None:
        self._image_size = value

    @hybrid_property
    def created_at(self: Self):
        return self._created_at

    @created_at.setter
    def created_at(self: Self, value) -> None:
        self._created_at = value
