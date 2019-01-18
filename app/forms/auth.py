# -*- coding: utf-8 -*-
from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models.user import User

_Author_ = 'BUPPT'


class RegisterForm(Form):
    email = StringField(validators=[
        DataRequired(),
        Length(6, 64),
        Email()
    ])

    password = PasswordField(validators=[
        DataRequired(),
        Length(6, 32),
        EqualTo('password2')
    ])

    password2 = PasswordField(validators=[
        DataRequired(),
        Length(6, 32)
    ])

    title = StringField(validators=[
        DataRequired()
    ])

    first_name = StringField(validators=[
        DataRequired()
    ])

    middle_name = StringField()

    last_name = StringField(validators=[
        DataRequired()
    ])

    degree = StringField()

    nick_name = StringField()

    phone_number = StringField()

    fax_number = StringField()

    secondary_email = StringField()

    institution_phone_number = StringField()

    institution = StringField()

    department = StringField()

    street_address = StringField(validators=[
        DataRequired()
    ])

    city = StringField(validators=[
        DataRequired()
    ])

    country = StringField(validators=[
        DataRequired()
    ])

    state_or_province = StringField()

    zip = StringField()

    person_keywords = StringField(validators=[
        DataRequired()
    ])

    person_keywords1 = StringField()
    person_keywords2 = StringField()
    person_keywords3 = StringField()
    person_keywords4 = StringField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("This Email has been registered")

    # def validate_secondary_email(self, field):
    #     if User.query.filter_by(secondary_email=field.data).first():
    #         raise ValidationError("This Email has existed")
    #
    # def validate_nick_name(self, field):
    #     if User.query.filter_by(nick_name=field.data).first():
    #         raise ValidationError("This nickname has existed")


class LoginForm(Form):
    email = StringField(validators=[
        DataRequired(),
        Length(6, 64),
        Email()
    ])

    password = PasswordField(validators=[
        DataRequired(message="please input your password"),
        Length(6, 32)
    ])
