# -*- coding: utf-8 -*-
from app.web import web

_Author_ = 'BUPPT'


@web.route("/")
def login():
    return "hello"
