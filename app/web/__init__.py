# -*- coding: utf-8 -*-
from flask import Blueprint

from app.models.models import Permission

_Author_ = 'BUPPT'

web = Blueprint('web', __name__)

from . import auth, home


@web.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
