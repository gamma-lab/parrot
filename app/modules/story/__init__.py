from flask import Blueprint, url_for, redirect
from flask_login import current_user

story = Blueprint('story', __name__, url_prefix='/story')


@story.before_request
def check_current_domain():
    if not current_user.current_domain_id:
        return redirect(url_for('domain.all_domains'))


from . import views
