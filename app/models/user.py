# -*- coding: utf-8 -*-
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.base import Base

_Author_ = 'BUPPT'


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    _password = Column(String(32), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    first_name = Column(String(32), nullable=False)
    middle_name = Column(String(32))
    last_name = Column(String(32), nullable=False)
    title = Column(String(16), nullable=False)
    degree = Column(String(16))
    nick_name = Column(String(32), unique=True)
    phone_num = Column(String(16))
    country = Column(String(16), nullable=False)
    city = Column(String(16), nullable=False)
    street = Column(String(64))
    # person_classifications   todo:这个键作为单独的一张表
    person_keywords = Column(Text, nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)
