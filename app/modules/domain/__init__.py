from flask import Blueprint

domain = Blueprint('domain', __name__, url_prefix='/domain')

from . import views
