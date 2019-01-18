# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user

from app.forms.auth import RegisterForm, LoginForm
from app.models.base import db
from app.models.user import User
from app.web import web

_Author_ = 'BUPPT'


@web.route("/")
def index():
    return render_template('index.html')


@web.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
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
            db.session.add(user)

        return redirect(url_for('web.login'))

    return render_template("auth/register.html", form=form)


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
            flash("Account is not existed or Password is wrong")
    return render_template('auth/login.html')
