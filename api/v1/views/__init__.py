#!/usr/bin/python3

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.student import *
from api.v1.views.subjects import *
from api.v1.views.teacher import *
from api.v1.views.user import *
