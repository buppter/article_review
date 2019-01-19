# -*- coding: utf-8 -*-
from flask import Blueprint

_Author_ = 'BUPPT'

web = Blueprint('web', __name__)

from . import auth, home
