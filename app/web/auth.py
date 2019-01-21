# -*- coding: utf-8 -*-
import datetime

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from app import cache
from app.forms.auth import RegisterForm, LoginForm
from app.models.base import db
from app.models.user import User, CountryList, Permission
from app.web import web

_Author_ = 'BUPPT'


@web.route("/")
@cache.cached(timeout=60, key_prefix="index")
def index():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('index.html', time=time)


@web.route("/register", methods=["GET", "POST"])
@cache.cached(timeout=60 * 60)
def register():
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
            user = User()
            user.set_attrs(form.data)
            user.person_keywords = keywords
            if data["is_reviewer"] == 1:
                user.role.add_permission(Permission.REVIEWER)
            db.session.add(user)

        return redirect(url_for('web.login'))

    return render_template("auth/register.html", form=form, all_countries=all_countries, time=time)


@web.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        is_auth = user.role.permissions & form.data['role'] == form.data['role']
        if user and user.check_password(form.password.data) and is_auth:
            login_user(user, remember=True)
            next_url = request.args.get('next')
            if not next_url or not next_url.startswith('/'):
                next_url = url_for("web.index")
            return redirect(next_url)
        else:
            flash("Account is not existed or Password is wrong")
    return render_template('auth/login.html')


@web.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("web.index"))
