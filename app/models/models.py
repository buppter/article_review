# -*- coding: utf-8 -*-
from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.models.base import Base, db

_Author_ = 'BUPPT'


class Permission:
    AUTHOR = 2
    REVIEWER = 4
    EDITOR = 8
    ADMIN = 16


user_roles = db.Table('user_roles',
                      db.Column('user_id', db.Integer, db.ForeignKey("users.id")),
                      db.Column('role_id', db.Integer, db.ForeignKey("roles.id")))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    def __repr__(self):
        return '<Role id={0}, name={1}>'.format(self.id, self.name)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'Author': [Permission.AUTHOR],
            'Reviewer': [Permission.REVIEWER],
            'Associate Editor': [Permission.EDITOR],
            'Editor-In-Chief': [Permission.ADMIN],
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
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm


class User(db.Model, Base, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    _password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), nullable=False, unique=True)
    first_name = db.Column(db.String(32), nullable=False)
    middle_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32), nullable=False)
    title = db.Column(db.String(16), nullable=False)
    degree = db.Column(db.String(16))
    # nick_name = db.Column(db.String(32))
    phone_number = db.Column(db.String(16))
    fax_number = db.Column(db.String(16))
    secondary_email = db.Column(db.String(64))
    institution_phone_number = db.Column(db.String(16))
    institution = db.Column(db.String(32))
    department = db.Column(db.String(32))
    street = db.Column(db.String(64))
    city = db.Column(db.String(16), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))
    state_or_province = db.Column(db.String(16))
    zip = db.Column(db.String(32))
    # person_classifications   todo:这个键作为单独的一张表
    person_keywords = db.Column(db.Text, nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))

    # article = db.relationship('NewSubmission', back_populates='uid')
    # editor_in_chief = db.relationship('NewSubmission', back_populates='editor_in_chief')
    # associate_editor = db.relationship('NewSubmission', back_populates='associate_editor')
    def __repr__(self):
        return '<User id={0}, email={1}, roles={2}>'.format(self.id, self.email, self.roles)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.roles:
            if self.email in current_app.config['ADMIN_EMAIL']:
                self.roles.append(Role.query.filter_by(permissions=Permission.ADMIN).first())
            if not self.roles:
                self.roles.append(Role.query.filter_by(default=True).first())

    @property
    def password(self):
        return AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def can(self, perm):
        role = Role.query.filter_by(permissions=perm).first()
        if role in self.roles:
            return True
        else:
            return False

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
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(16), nullable=False)
    country_name = db.Column(db.String(256), nullable=False)
    users = db.relationship("User", backref="country")

    def __repr__(self):
        return '<Country id={0}, country_code={1}, country_name={2}>'.format(self.id, self.country_code,
                                                                             self.country_name)


class NewSubmission(db.Model, Base):
    __tablename__ = 'new_submission'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    editor_in_chief_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    associate_editor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    type_id = db.Column(db.Integer, db.ForeignKey('article_type.id'))
    title = db.Column(db.String(256), nullable=False)
    abstract = db.Column(db.Text)
    keywords = db.Column(db.Text)
    # classification_id  TODO: 此键表还未建
    comments = db.Column(db.Text)
    current_status = db.Column(db.Integer)
    final_disposition = db.Column(db.Integer)
    editor_decision = db.Column(db.Integer)
    uid = db.relationship("User", foreign_keys='NewSubmission.user_id', backref='articles')
    editor_in_chief = db.relationship("User", foreign_keys='NewSubmission.editor_in_chief_id',
                                      backref='editor_in_chief')
    associate_editor = db.relationship("User", foreign_keys='NewSubmission.associate_editor_id',
                                       backref='associate_editor')

    @property
    def article_id(self):
        return "CC-{0}-{1}".format(datetime.now().year, self.id)

    def __repr__(self):
        return '<NewSubmission id={0}, title={1}, user={2}>'.format(self.article_id, self.title, self.uid)


class ArticleType(db.Model):
    __tablename__ = 'article_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    articles = db.relationship("NewSubmission", backref='type')

    def __repr__(self):
        return '<ArticleType id={0}, name={1}>'.format(self.id, self.name)
