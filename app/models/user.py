# -*- coding: utf-8 -*-
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.models.base import Base, db

_Author_ = 'BUPPT'


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    _password = Column(String(128), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    role_id = Column(Integer)
    first_name = Column(String(32), nullable=False)
    middle_name = Column(String(32))
    last_name = Column(String(32), nullable=False)
    title = Column(String(16), nullable=False)
    degree = Column(String(16))
    nick_name = Column(String(32))
    phone_number = Column(String(16))
    fax_number = Column(String(16))
    secondary_email = Column(String(64))
    institution_phone_number = Column(String(16))
    institution = Column(String(32))
    Department = Column(String(32))
    street = Column(String(64))
    city = Column(String(16), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"))
    state_or_province = Column(String(16))
    zip = Column(String(32))
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


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))


class CountryList(db.Model):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    country_code = Column(String(16), nullable=False)
    country_name = Column(String(256), nullable=False)
    users = relationship("User", backref="country")


class Role(db.Model):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(32), nullable=False)

