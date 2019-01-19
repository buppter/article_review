# -*- coding: utf-8 -*-
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.models.base import Base, db

_Author_ = 'BUPPT'


class Permission:
    AUTHOR = 1
    REVIEWER = 2
    EDITOR = 4
    ADMIN = 8


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 1

    @staticmethod
    def insert_roles():
        roles = {
            'Author': [Permission.AUTHOR],
            'Reviewer': [Permission.REVIEWER],
            'Editor': [Permission.EDITOR],
            'Admin': [Permission.ADMIN],
        }
        default_role = 'Author'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 1

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    _password = Column(String(128), nullable=False)
    email = Column(String(64), nullable=False, unique=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
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
    is_reviewer = Column(String(16), nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['SEEP_ADMIN']:
                self.role = Role.query.filter_by(name='Admin').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.can(Permission.ADMIN)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))


class CountryList(db.Model):
    __tablename__ = 'countries'
    id = Column(Integer, primary_key=True)
    country_code = Column(String(16), nullable=False)
    country_name = Column(String(256), nullable=False)
    users = relationship("User", backref="country")
