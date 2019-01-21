from flask import render_template
from flask_login import login_required

from app import cache
from app.web import web


@web.route("/home")
@login_required
def home():
    cache.delete('index')
    return render_template("home.html")

