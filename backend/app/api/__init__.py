from flask import Blueprint

bp = Blueprint('api', __name__)

from . import auth
from . import reminders  
from . import admin
from . import profile_routes