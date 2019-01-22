# -*- coding: utf-8 -*-
import datetime

from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user

from app import cache
from app.forms.auth import RegisterForm, LoginForm
from app.models.base import db
from app.models.user import User, CountryList, Permission, Role
from app.web import web

_Author_ = 'BUPPT'


@web.route("/")
# @cache.cached(timeout=60, key_prefix="index")
def index():
    return render_template('index.html')


@web.route("/register", methods=["GET", "POST"])
# @cache.cached(timeout=60 * 60)
def register():
    form = RegisterForm(request.form)
    all_countries = CountryList.query.all()
    if request.method == 'POST' and form.validate():
        data = form.data
        keywords = [data['person_keywords']]
        for i in range(1, 5):
            if data['person_keywords%s' % i] != '':
                keywords.append(data['person_keywords%s' % i])
        keywords = ",".join(keywords)

        with db.auto_commit():
            user = User(email=form.email.data)
            user.set_attrs(form.data)
            user.person_keywords = keywords
            if data["is_reviewer"] == 1:
                user.roles.append(Role.query.filter_by(name='Reviewer').first())
            db.session.add(user)

        return redirect(url_for('web.login'))

    return render_template("auth/register.html", form=form, all_countries=all_countries)


@web.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            next_url = request.args.get('next')
            if not next_url or not next_url.startswith('/'):
                next_url = url_for("web.index")
            return redirect(next_url)
        else:
            flash("Invalid username or password.")
    return render_template('auth/login.html', form=form)


@web.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("web.index"))
