# -*- coding: utf-8 -*-
from wtforms import Form, StringField, PasswordField, IntegerField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from app.models.user import User

_Author_ = 'BUPPT'


class RegisterForm(Form):
    email = StringField(validators=[
        DataRequired(message="Please input your email"),
        Length(6, 64),
        Email()
    ])

    password = PasswordField(validators=[
        DataRequired(message="Please input your password"),
        Length(6, 32),
        EqualTo('confirm_password', message="Passwords must match")
    ])

    confirm_password = PasswordField(validators=[
        DataRequired(message="Please confirm password"),
        Length(6, 32)
    ])

    title = StringField(validators=[
        DataRequired(message="Please choose a tile")
    ])

    first_name = StringField(validators=[
        DataRequired(message="Please input your first name")
    ])

    middle_name = StringField()

    last_name = StringField(validators=[
        DataRequired(message="Please input your lase name")
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
        DataRequired(message="Please input your street address")
    ])

    city = StringField(validators=[
        DataRequired(message="Please input your city")
    ])

    country_id = IntegerField(validators=[
        DataRequired(message="Please choose a country")
    ])

    state_or_province = StringField()

    zip = StringField()

    person_keywords = StringField(validators=[
        DataRequired(message="Please input a keyword at least")
    ])

    person_keywords1 = StringField()
    person_keywords2 = StringField()
    person_keywords3 = StringField()
    person_keywords4 = StringField()

    is_reviewer = IntegerField(
        validators=[
            DataRequired(message="Please choose whether you want to register as a reviewer")
        ])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("This Email has been registered")


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

    role = IntegerField(validators=[
        DataRequired(message="Please select your role")
    ])
