from flask import render_template
from flask_login import login_required

from app.web import web


@web.route("/home")
@login_required
def home():
    return render_template("home.html")

