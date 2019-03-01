from flask import render_template, redirect, url_for
from flask_login import current_user
# from ...model import Domain
from . import main
# from ... import db


@main.route('/')
def index():
    # if the user is logged in, redirect to dashboard
    return redirect(url_for('main.get_started'))
    # if current_user.current_domain_id:
    #     return redirect(url_for('domain.info_domain',
    #                             domain_id=current_user.current_domain_id))
    # elif len(current_user.domains):
    #     return redirect(url_for('domain.all_domains'))
    # else:
    #     return redirect(url_for('main.get_started'))


@main.route('/get_started')
def get_started():
    return render_template('main/get_started.html')
