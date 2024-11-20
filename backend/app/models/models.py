from sqlalchemy import (
    Column,
    Integer,
    String
)
from core import (
    ENUM_COLUMN_TABLE_USER, 
    ENUM_TABLE_DB,
    ENUM_MODEL_NAME,
    ENUM_ROLE
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from extension import ext

class Model_USER(ext.db_ext.Model):
    
    __tablename__ = ENUM_TABLE_DB.USER.value
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    _pseudo = Column(ENUM_COLUMN_TABLE_USER.PSEUDO.value, String, nullable=False)
    _email = Column(ENUM_COLUMN_TABLE_USER.EMAIL.value, String, nullable=False)
    _password_hash = Column(ENUM_COLUMN_TABLE_USER.PWD_HASH.value, String, nullable=False)
    _role_id = Column(ENUM_COLUMN_TABLE_USER.ROLE_ID.value, Integer, nullable=False)
    
    role = relationship(ENUM_MODEL_NAME.ROLE.value, back_populates=ENUM_TABLE_DB.USER.value)
    
    @hybrid_property
    def pseudo(self) -> str:
        return self._pseudo
    
    @hybrid_property
    def email(self) -> str:
        return self._email
    
    @hybrid_property
    def role_name(self):
        return self.role.role_name if self.role else None

    @role_name.expression
    def role_name(cls):
        return cls.role.has()

    @hybrid_property
    def is_admin(self):
        return self.role.role_name == ENUM_ROLE.ADMIN.value

    @is_admin.expression
    def is_admin(cls):
        return cls.role.has(role_name=ENUM_ROLE.ADMIN.value)


    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, value):
        self._password_hash = ext.pwd_context_ext.hash(value)
        
        
class Model_ROLE(ext.db_ext.Model):
    
    __tablename__ = ENUM_TABLE_DB.ROLE.value
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, unique=True, nullable=False)
    
    users = relationship(ENUM_MODEL_NAME.USER.value, back_populates=ENUM_TABLE_DB.ROLE.value)