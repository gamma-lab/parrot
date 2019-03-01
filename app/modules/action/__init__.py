from flask import Blueprint, url_for, redirect
from flask_login import current_user

action = Blueprint('action', __name__, url_prefix='/action')


@action.before_request
def check_current_domain():
    if not current_user.current_domain_id:
        return redirect(url_for('domain.all_domains'))


from . import views
